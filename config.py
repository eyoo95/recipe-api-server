class Config:
    JWT_SECRET_KEY = 'yhacademy1029##hello'  # 절대 노출시키면 안되는 키
    JWT_ACCESS_TOKEN_EXPIRES = False # True로 설정하면 3분의 유효기간이 생긴다.
    PROPAGATE_EXCEPTIONS = True # JWT가 예외처리를 해주는 옵션