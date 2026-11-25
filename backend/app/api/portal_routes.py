import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import PublicReport, User
from app.schemas import PublicReportCreate, PublicReportUpdate, PublicReportResponse
from app.auth import get_current_user, require_officer_or_admin

router = APIRouter(prefix="/api/portal", tags=["Public Environmental Portal"])

@router.post("/reports", response_model=PublicReportResponse, status_code=status.HTTP_201_CREATED)
def submit_public_report(report_in: PublicReportCreate, db: Session = Depends(get_db)):
    """
    Public citizen incident submission.
    Assigns unique trackable code for public status checking.
    """
    random_digits = random.randint(1000, 9999)
    report_code = f"ECO-REP-2026-{random_digits}"

    report = PublicReport(
        report_code=report_code,
        status="SUBMITTED",
        **report_in.dict()
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get("/reports", response_model=List[PublicReportResponse])
def list_public_reports(category: Optional[str] = None, db: Session = Depends(get_db)):
    """List public citizen complaints with optional category filter."""
    query = db.query(PublicReport)
    if category:
        query = query.filter(PublicReport.category == category.upper())
    return query.order_by(PublicReport.created_at.desc()).all()

@router.get("/reports/track/{report_code}", response_model=PublicReportResponse)
def track_report(report_code: str, db: Session = Depends(get_db)):
    """Look up public report by unique tracking code."""
    report = db.query(PublicReport).filter(PublicReport.report_code == report_code).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with code '{report_code}' was not found. Please verify your reference number."
        )
    return report

@router.put("/reports/{id}/status", response_model=PublicReportResponse)
def update_report_status(
    id: int,
    update_in: PublicReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_officer_or_admin)
):
    """Update citizen complaint verification status and notes (Officer/Admin)."""
    report = db.query(PublicReport).filter(PublicReport.id == id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    if update_in.status:
        report.status = update_in.status
    if update_in.verification_notes:
        report.verification_notes = update_in.verification_notes

    report.officer_id = current_user.id
    db.commit()
    db.refresh(report)
    return report
