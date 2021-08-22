# poleval-2021-question-answering

### Konfiguracja ELK
Zwiększenie limitu systemowego `mmap`: `sudo sysctl -w vm.max_map_count=262144`

### Konfiugracja rabbitmq
Logowanie się do dashboardu:
- login: `guest`
- hasło: `guest`

```
sudo docker run -p 5672:5672 -p 15672:15672 -it rabbitmq:3-management-alpine
```