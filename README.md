# FastKit Chat Example

Этот проект представляет собой пример реализации чата с использованием современных технологий и архитектурных подходов, таких как:

- **Unit of Work (UoW)** для управления транзакциями.
- **Dependency Injection (DI)** для внедрения зависимостей.
- **JWT-аутентификация** для защиты API.
- **Data-Driven Design** для работы с данными.
- **BaseRouter** и **BaseService** для модульной организации кода.

## Архитектура проекта

### 1. Unit of Work (UoW)
Используется для управления транзакциями и сессиями базы данных. Каждый репозиторий работает в рамках единой транзакции, что обеспечивает целостность данных.

### 2. Dependency Injection (DI)
Зависимости (например, сервисы и репозитории) внедряются через механизм DI, что делает код более модульным и тестируемым.

### 3. JWT-аутентификация
Для аутентификации пользователей используется JWT (JSON Web Token). Токены создаются при успешной аутентификации и используются для доступа к защищенным эндпоинтам.

### 4. Data-Driven Design
Проект построен вокруг данных: модели, схемы и репозитории обеспечивают четкое разделение ответственности и упрощают работу с данными.

### 5. BaseRouter и BaseService
- **BaseRouter** предоставляет базовую функциональность для маршрутов (например, CRUD-операции).
- **BaseService** инкапсулирует бизнес-логику и взаимодействует с репозиториями.
- **BaseRepository** инкапсулирует низкоуровневую реализацию репозиторий.

## Примеры кода

### 1. Маршруты (Routers)
Маршруты организованы с использованием **BaseRouter**. Например, `MessageRouter` для работы с сообщениями:

```python
from src.fastkit.routers.base import BaseRouter
from src.app.models.message import Message
from src.app.schemas.message import MessageCreate, MessageRead
from src.app.services.message import MessageService
from typing import Type

class MessageRouter(BaseRouter[Message, MessageCreate, MessageRead]):
    """Router for handling message operations."""

    def __init__(self, service_cls: Type[MessageService], prefix: str):
        super().__init__(service_cls, prefix, MessageCreate, MessageRead)
```
### 2. Гибкая настройка
Возможность полной настройки каждого слоя логики, без сложных действий. 

```python
class AuthRouter(BaseRouter[User, UserCreate, UserRead]):
    """Router for handling auth/user operations."""

    def __init__(self, service_cls: Type[AuthService], prefix: str):
        super().__init__(service_cls, prefix, UserCreate, UserRead)
        
        
        @self.router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Authorize: Public"]) 
        async def register(
            user_data: UserPublic = Depends(),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            service = self.service_cls(db_session)
            db_user = await service.register(user_data)
            return UserResponse.model_validate(db_user, from_attributes=True)


        @self.router.post("/login", status_code=status.HTTP_201_CREATED, tags=["Authorize: Public"]) 
        async def login(
            form_data: OAuth2PasswordRequestForm = Depends(),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            service = self.service_cls(db_session)
            return await service.login(form_data.username, form_data.password)
        

        @self.router.post("/protected", status_code=status.HTTP_201_CREATED, tags=["Authorize: Public"]) 
        async def protected(
            token: str = Depends(oauth2_scheme),
            db_session: AsyncSession = Depends(get_async_session),
        ):
            service = self.service_cls(db_session)
            return service.verify_token(token)
```


