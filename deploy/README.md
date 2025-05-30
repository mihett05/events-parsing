# Деплой

## На виртуальную машину
Чтобы развернуть приложение на VM нужно:
- Настроить переменные ansible в папке vars (домены и секреты, описание полей секретов есть в `vars/secrets.example.yaml`, секреты зашифровать через vault)
- Сохранить пароль от vault в `deploy/secrets.pass`
- Добавить ip в `deploy/hosts.ini`, в группу `[master]`
- Запусть плейбук `deploy/deploy-infra.yaml` для собственного registry и инфраструктуры: `ansible-playbook deploy/deploy-infra.yaml -i deploy/hosts.ini --vault-pass-file secrets.pass`
- Собрать и запушить образы: либо через ci, либо через `deploy/build.sh`
- Запустить плейбук `deploy/deploy.yaml`: `ansible-playbook deploy/deploy.yaml -i deploy/hosts.ini --vault-pass-file secrets.pass`