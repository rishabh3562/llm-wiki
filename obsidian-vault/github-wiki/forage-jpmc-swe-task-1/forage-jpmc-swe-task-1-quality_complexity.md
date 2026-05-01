---
repo: forage-jpmc-swe-task-1
type: quality_complexity
commit: 879221fec2b863d37d5b493f02a530a8098ef6ef
date: 2026-05-01
tags: [forage-jpmc-swe-task-1, quality_complexity]
related: [[forage-jpmc-swe-task-1-index]]
---

# Quality — Complexity Signals

## Evidence
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
    F 159:0 read_csv - A (2)
    F 194:0 read_params - A (2)
    F 219:0 run - A (2)
    C 170:0 ThreadedHTTPServer - A (2)
    M 284:4 App.read_10_first_lines - A (2)
    F 182:0 route - A (1)
    M 176:4 ThreadedHTTPServer.shutdown - A (1)
    M 257:4 App.__init__ - A (1)
client3.py
    F 32:0 getDataPoint - A (1)
    F 42:0 getRatio - A (1)



## Related
- [[forage-jpmc-swe-task-1-improvements]]
- [[forage-jpmc-swe-task-1-architecture]]
