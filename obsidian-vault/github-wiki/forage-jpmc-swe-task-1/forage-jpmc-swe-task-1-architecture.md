---
repo: forage-jpmc-swe-task-1
type: architecture
commit: 879221fec2b863d37d5b493f02a530a8098ef6ef
date: 2026-04-23
tags: [forage-jpmc-swe-task-1, architecture]
related: [[forage-jpmc-swe-task-1-index]]
---
# Architecture — forage-jpmc-swe-task-1
## Key Files (by size)

-rw-r--r-- 1 root root 84653 Apr 23 15:00 ./test.csv
-rw-r--r-- 1 root root 10765 Apr 23 15:00 ./server3.py
-rw-r--r-- 1 root root  2313 Apr 23 15:00 ./client3.py
-rw-r--r-- 1 root root  1167 Apr 23 15:00 ./client_test.py
-rw-r--r-- 1 root root    79 Apr 23 15:00 ./README.md
-rw-r--r-- 1 root root    22 Apr 23 15:00 ./requirements.txt

## High Churn Files
      5 
      2 README.md
      1 test.csv
      1 server3.py
      1 server.py
      1 requirements.txt
      1 client_test.py
      1 client3.py
      1 client.py

## Complexity
client_test.py
    C 4:0 ClientTest - A (2)
    M 5:2 ClientTest.test_getDataPoint_calculatePrice - A (1)
    M 12:2 ClientTest.test_getDataPoint_calculatePriceBidGreaterThanAsk - A (1)
server3.py
    M 290:4 App.handle_query - B (9)
    C 254:0 App - A (5)
    F 78:0 orders - A (4)
    F 102:0 clear_order - A (4)
    F 117:0 clear_book - A (4)
    F 204:0 get - A (4)
    M 267:4 App._current_book_1 - A (4)
    M 276:4 App._current_book_2 - A (4)
    F 94:0 add_book - A (3)
    F 132:0 order_book - A (3)
    F 149:0 generate_csv - A (3)
    F 61:0 bwalk - A (2)
    F 69:0 market - A (2)
    F 
