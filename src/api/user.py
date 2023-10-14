from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.post("login")
def user_log_in_handler():
    return "hello login"


@router.post("/sign-up", status_code=201)
def user_sign_up_handler():
    return "hello signup"


@router.post("/id")
def user_find_id_handler():
    return "hello id find"

@router.post("/password")
def user_find_password_handler():
    return "hello pw find"