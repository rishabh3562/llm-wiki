---
repo: Queue-Management-System
type: architecture
commit: 0724e65f41d92895177adb6028e5ae8b4009c6a5
date: 2026-05-02
tags: [Queue-Management-System, architecture]
related: [[Queue-Management-System-index]]
---

# Architecture — Queue-Management-System

## Key Files (by size)

-rw-r--r-- 1 root root 287630 May  2 01:01 ./staticfiles/admin/js/vendor/jquery/jquery.js
-rw-r--r-- 1 root root 232381 May  2 01:01 ./staticfiles/admin/js/vendor/xregexp/xregexp.js
-rw-r--r-- 1 root root 180224 May  2 01:01 ./db.sqlite3
-rw-r--r-- 1 root root 173566 May  2 01:01 ./staticfiles/admin/js/vendor/select2/select2.full.js
-rw-r--r-- 1 root root 125266 May  2 01:01 ./staticfiles/admin/js/vendor/xregexp/xregexp.min.js
-rw-r--r-- 1 root root  89476 May  2 01:01 ./staticfiles/admin/js/vendor/jquery/jquery.min.js
-rw-r--r-- 1 root root  86184 May  2 01:01 ./staticfiles/admin/fonts/Roboto
## High Churn Files
     17 
     15 README.md
      1 templates/view_queue.html
      1 templates/selectCounter.html
      1 templates/register.html
      1 templates/otp.html
      1 templates/login.html
      1 templates/index.html
      1 templates/employee.html
      1 staticfiles/admin/js/vendor/xregexp/xregexp.min.js
      1 staticfiles/admin/js/vendor/xregexp/xregexp.js
      1 staticfiles/admin/js/vendor/xregexp/LICENSE.txt
      1 staticfiles/admin/js/vendor/select2/select2.full.min.js
      1 staticfiles/admin/js/vendor/select2/select2.full.js
      1 staticfiles/admin/js/vendor/select2/i18n/zh-TW.js
 
## Complexity
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
app1/migr
