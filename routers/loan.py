from fastapi import APIRouter, Depends, HTTPException
from ..models import Loan, LoanCreate
from ..crud.loans import get_user_loans, create_loan, return_loan
from ..dependencies import get_current_user

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=Loan)
def create_loan_route(
    loan: LoanCreate,
    current_user: dict = Depends(get_current_user)
):
    try:
        loan_data = loan.dict()
        loan_data['user_id'] = current_user['user_id']
        return create_loan(loan_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-loans", response_model=list[Loan])
def read_user_loans(current_user: dict = Depends(get_current_user)):
    return get_user_loans(current_user['user_id'])

@router.post("/{loan_id}/return", response_model=Loan)
def return_loan_route(
    loan_id: int,
    current_user: dict = Depends(get_current_user)
):
    # Verify the loan belongs to the user
    loan = get_loan(loan_id)
    if not loan or loan['user_id'] != current_user['user_id']:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan['return_date']:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    return return_loan(loan_id)