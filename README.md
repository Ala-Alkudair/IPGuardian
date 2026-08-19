# IPGuardian Secure DevOps Log Analyzer

أداة بسيطة بلغة Python لتحليل ملفات **Log** الخاصة بمحاولات تسجيل الدخول، واكتشاف عناوين IP المشبوهة بناءً على تكرار محاولات الدخول الفاشلة، مبنية كمشروع تطبيقي لتعلم **Git / GitHub Workflow** و **DevOps Fundamentals**.

> تم بناء هذا المشروع كجزء من تدريب: **DevOps Fundamentals — Git & Collaborative Development Workshop**

---

## 1. نظرة عامة على المشروع

المشروع لا يركّز فقط على بناء أداة تحليل Logs، بل يركّز بشكل أساسي على تطبيق دورة تطوير برمجيات منظمة تشمل:

- Git & GitHub
- Feature Branching
- Commits منظمة
- Pull Requests و Code Review
- Automated Testing باستخدام Pytest
- CI (Continuous Integration) باستخدام GitHub Actions

## 2. فكرة الأداة

الأداة تقوم بالخطوات التالية:

1. قراءة ملف Log يحتوي على سجلات تسجيل دخول.
2. البحث عن كل سطر يحتوي على `Failed Login`.
3. استخراج عنوان الـ IP من السطر.
4. حساب عدد محاولات الدخول الفاشلة لكل IP.
5. اعتبار أي IP وصلت محاولاته الفاشلة إلى **3 أو أكثر** بأنه **Suspicious (مشبوه)**.

مثال:

```text
192.168.1.10 -> 3 Failed Login -> Suspicious
192.168.1.20 -> 0 Failed Login -> Normal
```

---

## 3. هيكل المشروع

```text
secure-DevOps-project/
│
├── app/
│   ├── __init__.py        # تعريف app كـ Python package
│   ├── log_parser.py      # منطق تحليل الـ Logs (الدالة الأساسية analyze_log_file)
│   └── __main__.py        # نقطة تشغيل CLI (python -m app)
│
├── tests/
│   └── test_parser.py     # اختبارات Pytest للدالة analyze_log_file
│
├── sample_logs/
│   └── auth.log           # ملف Log تجريبي لتجربة الأداة
│
├── .github/
│   └── workflows/
│       └── tests.yml      # GitHub Actions: تشغيل الاختبارات تلقائيًا
│
├── requirements.txt        # مكتبات المشروع
├── .gitignore
├── LICENSE
└── README.md
```

## 4. آلية عمل الكود (`app/log_parser.py`)

```python
FAILED_LOGIN_THRESHOLD = 3

def analyze_log_file(file_path):
    # يقرأ الملف سطر سطر
    # يبحث عن "Failed Login"
    # يستخرج IP بصيغة xxx.xxx.xxx.xxx بواسطة Regex
    # يحسب عدد المحاولات الفاشلة لكل IP
    # يرجع dict فيه كل المحاولات، و dict ثاني فيه الـ IPs المشبوهة فقط
    ...
```

الدالة `analyze_log_file` ترجع:

```python
{
    "failed_attempts": {"192.168.1.10": 3, "192.168.1.30": 4},
    "suspicious_ips":  {"192.168.1.10": 3, "192.168.1.30": 4},
}
```

---

## 5. المتطلبات (Requirements)

- Python 3.10 أو أحدث
- pip

## 6. طريقة التشغيل (Installation & Usage)

### أ. تحميل المشروع

```bash
git clone https://github.com/Ala-Alkudair/secure-DevOps-project.git
cd secure-DevOps-project
```

### ب. إنشاء وتفعيل بيئة افتراضية (Virtual Environment)

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ج. تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### د. تشغيل الأداة

تشغيل الأداة على ملف الـ Log التجريبي المرفق:

```bash
python -m app
```

أو على ملف Log مخصص:

```bash
python -m app path/to/your_logfile.log
```

مثال على الناتج:

```text
192.168.1.10 -> 3 Failed Login -> Suspicious
192.168.1.30 -> 4 Failed Login -> Suspicious
```

---

## 7. تشغيل الاختبارات (Testing)

المشروع يستخدم **Pytest**. الاختبارات موجودة في `tests/test_parser.py` وتغطي:

| الاختبار | الهدف |
| --- | --- |
| `test_detect_suspicious_ip` | IP بثلاث محاولات فاشلة أو أكثر يُصنَّف Suspicious |
| `test_ip_below_threshold_is_not_suspicious` | IP بمحاولتين فقط لا يُصنَّف Suspicious |
| `test_successful_login_is_not_counted` | `Successful Login` لا يُحتسب ضمن المحاولات الفاشلة |
| `test_sample_log_file_matches_expected_results` | تشغيل الدالة على `sample_logs/auth.log` الفعلي والتأكد من صحة النتيجة |

تشغيل الاختبارات:

```bash
python -m pytest -v
```

النتيجة المتوقعة:

```text
4 passed
```

> **ملاحظة (Known Issue):** تشغيل `pytest -v` مباشرة (بدون `python -m`) قد يعطي `ModuleNotFoundError: No module named 'app'` على بعض الإعدادات، لأن الأمر المباشر لا يضيف جذر المشروع تلقائيًا إلى `sys.path` كما يفعل `python -m pytest`. الحل الموصى به: استخدام `python -m pytest -v` دائمًا، أو إضافة إعداد `pythonpath` في `pyproject.toml`.

---

## 8. CI/CD — GitHub Actions

تم إعداد Workflow في:

```text
.github/workflows/tests.yml
```

يقوم تلقائيًا بما يلي عند كل `push` أو `pull request` باتجاه `main`:

1. تجهيز بيئة Ubuntu.
2. تثبيت Python.
3. تثبيت المكتبات من `requirements.txt`.
4. تشغيل `pytest -v`.

هذا يضمن أن أي تعديل جديد لا يكسر الاختبارات الحالية قبل دمجه في `main`.

---

## 9. Git Workflow المتبع

```text
Create Repository
      ↓
Create .gitignore / README / LICENSE
      ↓
Create Virtual Environment
      ↓
Create Feature Branch (feature/project-setup)
      ↓
Build Project Structure → Commit → Push
      ↓
Pull Request → Code Review → Merge into main
      ↓
Create New Feature Branch (feature/log-analyzer)
      ↓
Develop Log Analyzer + Tests + CLI + CI
      ↓
Commit → Push → Pull Request → Merge
```

### Branches

| Branch | الهدف | الحالة |
| --- | --- | --- |
| `main` | الفرع الرئيسي المستقر | نشط |
| `feature/project-setup` | إنشاء هيكل المشروع الأساسي | تم دمجه في `main` (PR #1) |
| `feature/log-analyzer` | تطوير أداة تحليل الـ Logs، الاختبارات، الـ CLI، والـ CI | قيد التطوير |

---

## 10. مشاكل واجهتها الحلول (Problems & Solutions)

### مشكلة: `fatal: repository 'YOUR_REPOSITORY_URL' does not exist`

**السبب:** تنفيذ `git clone` باستخدام رابط Placeholder وليس رابطًا حقيقيًا.
**الحل:** تم تجاهل الأمر لأن المشروع كان موجودًا محليًا بالفعل.

### مشكلة: `Author identity unknown` عند أول Commit

**السبب:** Git لا يعرف اسم المستخدم والإيميل.
**الحل:**

```bash
git config --global user.name "your-name"
git config --global user.email "your-email@example.com"
```

### مشكلة: `ModuleNotFoundError: No module named 'app'` عند تشغيل الاختبارات

**السبب:** تم تشغيل `pytest` قبل اكتمال هيكلة المشروع (`app/__init__.py`)، وأيضًا فرق سلوك `pytest` مقابل `python -m pytest` بخصوص إضافة جذر المشروع إلى `sys.path`.
**الحل:** التأكد من وجود `app/__init__.py`، واستخدام `python -m pytest -v` لتشغيل الاختبارات.

### مشكلة: ترميز خاطئ في `requirements.txt` (UTF-16 بدل UTF-8)

**السبب:** الأمر `pip freeze > requirements.txt` عند تنفيذه داخل PowerShell يحفظ الملف افتراضيًا بترميز `UTF-16 LE`، مما قد يسبب فشل تثبيت المكتبات على بيئات Linux مثل GitHub Actions.
**الحل:** إعادة كتابة الملف بترميز UTF-8 عادي. لتفادي المشكلة مستقبلًا:

```powershell
pip freeze | Out-File -Encoding utf8 requirements.txt
```

---

## 11. التقنيات المستخدمة

- **Python** — لغة البرمجة الأساسية
- **Pytest** — Automated Testing
- **Git & GitHub** — إدارة الإصدارات والتعاون
- **GitHub Actions** — CI (تشغيل الاختبارات تلقائيًا)

## 12. تحسينات مستقبلية (Future Improvements)

- إضافة دعم لأنماط Logs مختلفة (مثل صيغ JSON أو Syslog).
- إمكانية تصدير النتائج إلى CSV / JSON.
- إضافة Badge لحالة GitHub Actions في هذا الملف.
- إضافة GitHub Issues لتتبع المهام المستقبلية.
- إضافة Deployment step (مثال: نشر كأداة CLI عبر PyPI).

---

## License

هذا المشروع مرخّص تحت [MIT License](LICENSE).
