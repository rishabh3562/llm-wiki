---
repo: forage-jpmc-swe-task-1
type: static_analysis
commit: 879221fec2b863d37d5b493f02a530a8098ef6ef
date: 2026-04-23
tags: [forage-jpmc-swe-task-1, static_analysis]
related: [[forage-jpmc-swe-task-1-index]]
---
{
  "largest_files": "-rw-r--r-- 1 root root 84653 Apr 23 15:00 ./test.csv\n-rw-r--r-- 1 root root 10765 Apr 23 15:00 ./server3.py\n-rw-r--r-- 1 root root  2313 Apr 23 15:00 ./client3.py\n-rw-r--r-- 1 root root  1167 Apr 23 15:00 ./client_test.py\n-rw-r--r-- 1 root root    79 Apr 23 15:00 ./README.md\n-rw-r--r-- 1 root root    22 Apr 23 15:00 ./requirements.txt\n",
  "high_churn_files": "      5 \n      2 README.md\n      1 test.csv\n      1 server3.py\n      1 server.py\n      1 requirements.txt\n      1 client_test.py\n      1 client3.py\n      1 client.py\n",
  "complexity": "client_test.py\n    C 4:0 ClientTest - A (2)\n    M 5:2 ClientTest.test_getDataPoint_calculatePrice - A (1)\n    M 12:2 ClientTest.test_getDataPoint_calculatePriceBidGreaterThanAsk - A (1)\nserver3.py\n    M 290:4 App.handle_query - B (9)\n    C 254:0 App - A (5)\n    F 78:0 orders - A (4)\n    F 102:0 clear_order - A (4)\n    F 117:0 clear_book - A (4)\n    F 204:0 get - A (4)\n    M 267:4 App._current_book_1 - A (4)\n    M 276:4 App._current_book_2 - A (4)\n    F 94:0 add_book - A (3)\n    F 132:0 order_book - A (3)\n    F 149:0 generate_csv - A (3)\n    F 61:0 bwalk - A (2)\n    F 69:0 market - A (2)\n    F 159:0 read_csv - A (2)\n    F 194:0 read_params - A (2)\n    F 219:0 run - A (2)\n    C 170:0 ThreadedHTTPServer - A (2)\n    M 284:4 App.read_10_first_lines - A (2)\n    F 182:0 route - A (1)\n    M 176:4 ThreadedHTTPServer.shutdown - A (1)\n    M 257:4 App.__init__ - A (1)\nclient3.py\n    F 32:0 getDataPoint - A (1)\n    F 42:0 getRatio - A (1)\n\n",
  "dead_code": "client3.py:42: unused variable 'price_a' (100% confidence)\nclient3.py:42: unused variable 'price_b' (100% confidence)\nserver3.py:174: unused variable 'allow_reuse_address' (60% confidence)\nserver3.py:225: unused method 'log_message' (60% confidence)\nserver3.py:225: unused variable 'args' (100% confidence)\nserver3.py:225: unused variable 'kwargs' (100% confidence)\nserver3.py:228: unused method 'do_GET' (60% confidence)\nserver3.py:239: unreachable code after 'while' (100% confidence)\nserver3.py:248: unused variable 'ops' (60% confidence)\nserver3.py:289: unused method 'handle_query' (60% confidence)\n"
}