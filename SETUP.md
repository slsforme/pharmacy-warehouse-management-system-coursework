# Настройка проекта


### Генерация secret-key
**linux через openssl, кодировка base64:**
```
openssl rand -base64 48
```

**poetry через cmd:**
```
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**без poetry через cmd:**
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```