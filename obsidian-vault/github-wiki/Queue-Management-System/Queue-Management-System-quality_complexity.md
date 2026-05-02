---
repo: Queue-Management-System
type: quality_complexity
commit: 0724e65f41d92895177adb6028e5ae8b4009c6a5
date: 2026-05-02
tags: [Queue-Management-System, quality_complexity]
related: [[Queue-Management-System-index]]
---

# Quality — Complexity Signals

## Evidence
manage.py
    F 7:0 main - A (2)
app1/apps.py
    C 3:0 App1Config - A (1)
app1/views.py
    F 238:0 employee - C (16)
    F 314:0 selectCounter - B (10)
    F 50:0 register - B (9)
    F 199:0 logout - B (7)
    F 116:0 otp - A (5)
    F 167:0 view_queue - A (4)
    F 183:0 login - A (3)
    F 46:0 index - A (1)
app1/models.py
    C 10:0 Employee - A (2)
    C 18:0 userData - A (2)
    M 14:4 Employee.__str__ - A (1)
    M 28:4 userData.__str__ - A (1)
    C 32:0 num_counters - A (1)
app1/migrations/0010_alter_employee_counternumber_alter_employee_user.py
    C 9:0 Migration - A (1)
app1/migrations/0004_userdata_token.py
    C 6:0 Migration - A (1)
app1/migrations/0006_remove_employee_department_employee_counternumber.py
    C 6:0 Migration - A (1)
app1/migrations/0007_remove_employee_counternumber_remove_employee_user_and_more.py
    C 6:0 Migration - A (1)
app1/migrations/0003_auto_20211206_2354.py
    C 6:0 Migration - A (1)
app1/migrations/0001_initial.py


## Related
- [[Queue-Management-System-improvements]]
- [[Queue-Management-System-architecture]]
