from fastapi import APIRouter, Depends, HTTPException
from ..models import Loan, LoanCreate
from ..crud.loans import get_user_loans, create_loan, return_loan, get_loan, update_loan, delete_loan
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
    #verification
    loan = get_loan(loan_id)
    if not loan or loan['user_id'] != current_user['user_id']:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan['return_date']:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    return return_loan(loan_id)

@router.put("/{loan_id}")
def update_loan_route(loan_id: int, loan_data: dict):
    updated_loan = update_loan(loan_id, loan_data)
    if not updated_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return updated_loan

@router.delete("/{loan_id}")
def delete_loan_route(loan_id: int):
    if not delete_loan(loan_id):
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Loan deleted successfully"}