---
repo: Sentiment-analyzer
type: static_analysis
commit: a697f11fa97e82dd60c5a2dae39e7fd576a8a6ab
date: 2026-04-23
tags: [Sentiment-analyzer, static_analysis]
related: [[Sentiment-analyzer-index]]
---
{
  "largest_files": "-rw-r--r-- 1 root root 2015733 Apr 23 12:07 ./model/emotion_classifier_pipeline.pkl\n-rw-r--r-- 1 root root   73251 Apr 23 12:07 ./notebooks/EmotionDetection.ipynb\n-rw-r--r-- 1 root root    3084 Apr 23 12:07 ./.gitignore\n-rw-r--r-- 1 root root    1653 Apr 23 12:07 ./app.py\n-rw-r--r-- 1 root root    1068 Apr 23 12:07 ./LICENSE\n-rw-r--r-- 1 root root      66 Apr 23 12:07 ./.gitattributes\n-rw-r--r-- 1 root root      54 Apr 23 12:07 ./README.md\n",
  "high_churn_files": "      2 .gitignore\n      2 \n      1 notebooks/EmotionDetection.ipynb\n      1 model/emotion_classifier_pipeline.pkl\n      1 app.py\n      1 README.md\n      1 LICENSE\n      1 .gitattributes\n",
  "complexity": "app.py\n    F 20:0 main - A (4)\n    F 10:0 predict_emotions - A (1)\n    F 14:0 get_prediction_proba - A (1)\n\n3 blocks (classes, functions, methods) analyzed.\nAverage complexity: A (2.0)\n",
  "dead_code": "app.py:3: unused import 'pd' (90% confidence)\napp.py:4: unused import 'np' (90% confidence)\n"
}