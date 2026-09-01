import asyncio
from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import AsyncSessionLocal
from app.models.entities import Opportunity, DeadlineEvent, Notification

async def check_deadlines() -> None:
    """
    Scheduled background job to check active opportunities
    and generate deadline notifications.
    """
    async with AsyncSessionLocal() as db:
        now = datetime.utcnow()
        # Find opportunities closing in the next 7 days
        stmt = select(Opportunity).where(
            Opportunity.deadline != None,
            Opportunity.status.in_(["NEW", "OPEN", "CLOSING_SOON"])
        )
        result = await db.execute(stmt)
        opportunities = result.scalars().all()

        for op in opportunities:
            if not op.deadline:
                continue
                
            days_left = (op.deadline - now).days
            
            # Update status if expired
            if days_left < 0:
                op.status = "EXPIRED"
                db.add(op)
                continue
                
            if days_left <= 3 and op.status != "CLOSING_SOON":
                op.status = "CLOSING_SOON"
                db.add(op)
                
            # Create deadline events / notifications if they don't exist
            # This is a simplified check
            # In a production system, we'd query DeadlineEvent to avoid duplicates
            if days_left in [7, 3, 1, 0]:
                event_check = await db.execute(
                    select(DeadlineEvent).where(
                        DeadlineEvent.opportunity_id == op.id,
                        DeadlineEvent.days_remaining == days_left
                    )
                )
                if not event_check.scalars().first():
                    event = DeadlineEvent(
                        opportunity_id=op.id,
                        deadline_date=op.deadline,
                        days_remaining=days_left,
                        notification_triggered=True
                    )
                    db.add(event)
                    
                    # Notify users who have this in their pipeline
                    # We'd find applications for this op.id and create notifications
                    pass

        await db.commit()

async def start_background_tasks():
    """
    Simple async loop to run scheduled tasks in the background.
    In a real large-scale deployment, we'd use Celery + Redis.
    """
    while True:
        try:
            await check_deadlines()
        except Exception as e:
            print(f"Background task error: {e}")
        
        # Run once per day (or hour for testing)
        await asyncio.sleep(60 * 60)
