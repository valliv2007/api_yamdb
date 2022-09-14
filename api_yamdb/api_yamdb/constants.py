MAX_SCORE = 10
MIN_SCORE = 1
MESSAGE_ERR_SCORE = f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}'
USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = ((USER, 'Аутентифицированный пользователь'),
         (MODERATOR, 'Модератор'),
         (ADMIN, 'Администратор'))
FORBIDDEN_USERNAME = 'me'
