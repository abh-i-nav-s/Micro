from flask import Flask, render_template_string, request, redirect, url_for
import random, html, json, re

app = Flask(__name__)

# ------------------------
# BUG SNIPPETS (50 items)
# ------------------------
BUGS = [
    {"code": ["def greet(name)", "    if name:", "        print('Hello', name)", "    else:", "        print('No name')"], "correct_line": 1},
    {"code": ["numbers = [1, 2, 3, 4]", "total = 0", "for i in numbers", "    total += i", "print(total)"], "correct_line": 3},
    {"code": ["def add(a, b):", "    return a + b", "", "print(add(5))"], "correct_line": 4},
    {"code": ["for i in range(3):", "print('Value:', i)", "    print('Done loop')"], "correct_line": 2},
    {"code": ["x = 10", "y = 0", "if y != 0:", "    print(x / y)", "else:", "    print('Cannot divide')"], "correct_line": 4},
    {"code": ["def find_max(nums):", "    max_num = nums[0]", "    for n in nums:", "        if n > max_num:", "        max_num = n", "    return max_num"], "correct_line": 5},
    {"code": ["x = [1, 2, 3]", "for i in range(4):", "    print(x[i])", "print('Done')"], "correct_line": 3},
    {"code": ["def say_hello():", "    print('Hello')", "  print('Welcome!')", "say_hello()"], "correct_line": 3},
    {"code": ["for i in range(5)", "    print('Loop:', i)", "print('Finished')"], "correct_line": 1},
    {"code": ["name = input('Enter name: ')", "if name = 'John':", "    print('Hi John!')", "else:", "    print('Not John')"], "correct_line": 2},
    {"code": ["def multiply(a, b):", "    result = a * b", "    return result", "print(result)"], "correct_line": 4},
    {"code": ["x = 5", "if x > 2", "    print('Big number')", "print('Done')"], "correct_line": 2},
    {"code": ["def greet_user(name):", "    print('Welcome, ' + name)", "greet_user()"], "correct_line": 3},
    {"code": ["items = ['pen', 'book', 'pencil']", "for item in items:", "print(item)", "print('End')"], "correct_line": 3},
    {"code": ["x = 10", "y = 5", "if x > y:", "print('x is greater')", "    print('Comparison done')"], "correct_line": 4},
    {"code": ["def check_even(num):", "    if num % 2 == 0:", "        print('Even')", "    else", "        print('Odd')"], "correct_line": 4},
    {"code": ["student = {'name': 'Raj', 'age': 20}", "print(student[name])"], "correct_line": 2},
    {"code": ["def divide(a, b):", "    if b == 0:", "        print('Cannot divide by zero')", "    else:", "        return a / b", "print(divide(5, 0)"], "correct_line": 6},
    {"code": ["x = 3", "while x > 0:", "print(x)", "x -= 1"], "correct_line": 3},
    {"code": ["def get_area(radius):", "    area = 3.14 * radius ** 2", "    print('Area:', area)", "getarea(5)"], "correct_line": 4},
    {"code": ["for i in range(3):", "    for j in range(3):", "    print(i, j)", "print('Done')"], "correct_line": 3},
    {"code": ["def welcome(name):", "print('Hello', name)", "print('Done')"], "correct_line": 2},
    {"code": ["x = [1, 2, 3]", "print(x(0))", "print('ok')"], "correct_line": 2},
    {"code": ["for i in range(5):", "    if i == 3", "        print('Found 3')", "print('Loop Ended')"], "correct_line": 2},
    {"code": ["def factorial(n):", "    if n == 0:", "        return 1", "    else:", "        return n * factorial(n-1)", "print(factorial())"], "correct_line": 6},
    {"code": ["x = 10", "y = 20", "if x > y:", "    print('X big')", "else:", "print('Y big')"], "correct_line": 6},
    {"code": ["numbers = [10, 20, 30]", "for n in numbers", "    print(n)"], "correct_line": 2},
    {"code": ["def cube(x):", "    return x *** 3", "print(cube(2))"], "correct_line": 2},
    {"code": ["a = 5", "b = 0", "c = a / b", "print(c)"], "correct_line": 3},
    {"code": ["def sum_list(lst):", "    total = 0", "    for i in lst:", "        total = total + i", "    print(total)", "sum_list()"], "correct_line": 6},
    {"code": ["for i in range(3):", "    for j in range(3):", "        print(i, j)", "    print('Inner loop done')", "print('Outer done')"], "correct_line": 5},
    {"code": ["x = 5", "if x == 5:", "print('Correct')", "else:", "print('Wrong')"], "correct_line": 3},
    {"code": ["def hello():", "    print('Hello')", "print('Bye')", "Hello()"], "correct_line": 4},
    {"code": ["a = [1, 2, 3]", "for i in range(3):", "    print(a[i])", "print(a[3])"], "correct_line": 4},
    {"code": ["def add(a, b):", "    result = a + b", "return result"], "correct_line": 3},
    {"code": ["x = 10", "if x > 5:", "    print('Yes')", " else:", "    print('No')"], "correct_line": 4},
    {"code": ["def square(num):", "    result = num ** 2", "    return result", "print(result(5))"], "correct_line": 4},
    {"code": ["def main():", "    print('Start')", "if __name__ == '__main__'", "    main()"], "correct_line": 3},
    {"code": ["x = 1", "while x < 5:", "    print(x)", "x += 1"], "correct_line": 4},
    {"code": ["try:", "    print(10/0)", "except:", "print('Error')"], "correct_line": 4},
    {"code": ["def greet(msg='Hi')", "    print(msg)", "greet()"], "correct_line": 1},
    {"code": ["x = int(input('Enter: '))", "if x % 2 == 0:", "    print('Even')", "else:", "print('Odd')"], "correct_line": 5},
    {"code": ["def product(a, b):", "    return a * b", "print(product(a, b))"], "correct_line": 3},
    {"code": ["for i in range(3):", "    print('Value:', i)", "    if i == 1:", "    print('Middle')"], "correct_line": 4},
    {"code": ["def display():", "print('Inside function')", "display()"], "correct_line": 2},
    {"code": ["x = 5", "y = 10", "if x > y print('x greater')"], "correct_line": 3},
    {"code": ["def greet():", "    print('Hello')", "greet(", "print('Done')"], "correct_line": 3},
    {"code": ["for i in range(2):", "    for j in range(2):", "        print(i,j)", "    print('Inner done')", "print('End'"], "correct_line": 5},
]

# ------------------------
# Heuristic explanation function
# ------------------------
def explain_bug(code_lines, bug_line_index):
    n = len(code_lines)
    if bug_line_index < 1 or bug_line_index > n:
        return "Could not determine the bug location."

    line = code_lines[bug_line_index - 1].strip()

    if re.search(r"\bif\b.*[^:]\s*$", line) or re.search(r"\bfor\b.*[^:]\s*$", line) or re.search(r"\bwhile\b.*[^:]\s*$", line) or line.endswith(")")==False and re.search(r"\bdef\b", line):
        if not line.endswith(":"):
            return f"Line {bug_line_index}: Missing colon at the end of a block statement."
    if "=" in line and re.match(r"\s*if\s+.*=.*:", line) or re.match(r".*\bif\b.*=.*", line):
        if re.search(r"\bif\b.*=.*", line) and not re.search(r"==", line):
            return f"Line {bug_line_index}: Using assignment '=' instead of '==' in a conditional."
    if ("print(" in line and line.count("(") != line.count(")")) or ("(" in line and ")" not in line):
        return f"Line {bug_line_index}: Unmatched or missing parenthesis."
    if re.search(r"\breturn\b", line) and not line.startswith(" "):
        return f"Line {bug_line_index}: Indentation error — 'return' should be indented inside the function."
    if re.search(r"\bprint\(", line) and re.search(r"print\([^\)]*$", line):
        return f"Line {bug_line_index}: Missing closing parenthesis in a print call."
    if re.search(r"\w+\[[^\]]+\]", line) and re.search(r"\w+\(", line):
        return f"Line {bug_line_index}: Using parentheses '()' instead of brackets '[]' for list indexing."
    if re.search(r"\*\*\*", line):
        return f"Line {bug_line_index}: Invalid operator '***' (should be '**' for power)."
    if re.search(r"print\([^\)]*\)$", line) and "result" in line and "(" not in line:
        return f"Line {bug_line_index}: Using a variable that doesn't exist in this scope."
    return f"Line {bug_line_index}: Likely a syntax or logic error in this line: \"{line}\""

# ------------------------
# Templates
# ------------------------
TEMPLATE_READY = r"""
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Bug Hunter — Ready</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{ --bg:#0f1724; --panel:#0b1220; --muted:#9aa4b2; --accent:#ffca28; --text:#dbe7ef; }
body{ margin:0; font-family:Inter, 'Fira Code', monospace; background:var(--bg); color:var(--text); }
.header{ padding:18px 22px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.03); }
.logo{ background:linear-gradient(135deg,#2b333b,#0b1220); padding:8px 12px; border-radius:8px; color:var(--accent); font-weight:800; }
.container{ max-width:900px; margin:30px auto; padding:18px; display:flex; gap:18px; }
.card{ background:linear-gradient(180deg,#06101a,#07111b); padding:16px; border-radius:12px; width:100%; border:1px solid rgba(255,255,255,0.02); }
.big{ font-size:40px; color:var(--accent); font-weight:800; }
.muted{ color:var(--muted); }
.btn{ background:var(--accent); color:#071021; padding:10px 16px; border-radius:8px; border:none; font-weight:800; cursor:pointer; }
.small{ background:transparent; color:var(--accent); border:1px solid rgba(255,255,255,0.04); padding:8px 12px; border-radius:8px; cursor:pointer; }
footer{ text-align:center; color:var(--muted); margin-top:28px; }
</style>
</head>
<body>
  <div class="header">
    <div class="logo">Bug Hunter</div>
  </div>
  <div class="container">
    <div class="card">
      <div class="muted">Current Player (randomly chosen)</div>
      <div class="big">{{ roll }}</div>
      <p class="muted">Click <strong>Play</strong> to hunt some bugs.</p>
      <form method="get" action="{{ url_for('question') }}">
        <input type="hidden" name="bug_idx" value="{{ bug_idx }}">
        <input type="hidden" name="roll" value="{{ roll }}">
        <button type="submit" class="btn">Play</button>
        <a class="small" href="{{ url_for('play') }}" style="margin-left:10px">Pick Another Roll</a>
      </form>
    </div>
  </div>
</body>
</html>
"""

TEMPLATE_QUESTION = r"""
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Bug Hunter — Question</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{ --bg:#0f1724; --panel:#0b1220; --muted:#9aa4b2; --accent:#ffca28; --text:#dbe7ef; --kw:#569cd6; --str:#98c379; --num:#d19a66; --cm:#6a737d; --fn:#dcdcaa; --gutter:#071021; --ide:#0b1320; }
body{ margin:0; font-family:Inter, 'Fira Code', monospace; background:var(--bg); color:var(--text); }
.header{ padding:14px 22px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.03); }
.logo{ background:linear-gradient(135deg,#2b333b,#0b1220); padding:8px 12px; border-radius:8px; color:var(--accent); font-weight:800; }
.container{ max-width:1100px; margin:20px auto; padding:18px; display:flex; gap:18px; align-items:flex-start; }
.ide{ flex:1; background:var(--panel); padding:12px; border-radius:12px; border:1px solid rgba(255,255,255,0.02); }
.ide-top{ display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.tabs{ display:flex; gap:8px; }
.tab{ background:rgba(255,255,255,0.02); padding:6px 10px; border-radius:8px; color:var(--muted); }
.toolbar{ display:flex; gap:10px; align-items:center; }
.timer{ background:#071022; padding:6px 10px; border-radius:8px; color:var(--accent); font-weight:800; }
.code-area{ display:flex; gap:12px; }
.gutter{ background:var(--gutter); padding:12px 8px; border-radius:8px; color:var(--muted); min-width:56px; text-align:right; }
.codebox{ background:var(--ide); padding:12px; border-radius:8px; overflow:auto; min-width:420px; box-shadow:inset 0 1px 0 rgba(255,255,255,0.02); }
pre{ margin:0; font-family:'Fira Code','Courier New',monospace; font-size:14px; line-height:1.45; white-space:pre; color:var(--text);}
.line{ display:block; padding:2px 6px; }
.kw{ color:var(--kw); font-weight:700; }
.str{ color:var(--str); }
.num{ color:var(--num); }
.cm{ color:var(--cm); font-style:italic; }
.fn{ color:var(--fn); }
.highlight{ background:rgba(255,77,79,0.12); border-left:4px solid rgba(255,77,79,0.9); border-radius:4px; padding-left:6px; }
.side{ width:320px; display:flex; flex-direction:column; gap:12px; }
.card{ background:linear-gradient(180deg,#06101a,#07111b); padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,0.02); }
.big{ font-size:28px; font-weight:800; color:var(--accent); }
.input{ margin-top:10px; display:flex; gap:8px; }
input[type=number]{ width:100%; padding:8px 10px; border-radius:8px; border:1px solid rgba(255,255,255,0.04); background:transparent; color:inherit; }
.btn{ background:var(--accent); color:#071021; padding:8px 12px; border-radius:8px; border:none; font-weight:800; cursor:pointer; }
.muted{ color:var(--muted); font-size:13px; }
footer{ text-align:center; color:var(--muted); margin-top:20px; }
@media (max-width:900px){ .container{ flex-direction:column; } .gutter{ display:none; } .side{ width:100%; } }
</style>
</head>
<body>
  <div class="header">
    <div style="display:flex;gap:12px;align-items:center"><div class="logo">Bug Hunter</div></div>
    <div class="muted">Roll no: <strong>{{ roll }}</strong></div>
  </div>

  <div class="container">
    <section class="ide">
      <div class="ide-top">
        <div class="tabs"><div class="tab">error.py</div></div>
        <div class="toolbar"><div id="timer" class="timer">20</div></div>
      </div>
      <div class="code-area">
        <div class="gutter" id="gutter" aria-hidden="true"></div>
        <div class="codebox">
          <pre id="codepre" aria-live="polite"></pre>
        </div>
      </div>
    </section>

    <aside class="side">
      <div class="card">
        <div class="muted">Tap to play</div>
        <div class="muted" style="margin-top:8px">Press <strong>Start</strong> to hunt.</div>
        <form id="answer-form" method="post" action="{{ url_for('result') }}">
          <input type="hidden" name="bug_idx" value="{{ bug_idx }}">
          <input type="hidden" name="roll" value="{{ roll }}">
          <input type="hidden" name="correct_line" id="correct_line" value="{{ bug['correct_line'] }}">
          <div style="margin-top:12px;">
            <button id="start-btn" type="button" class="btn">Start</button>
          </div>
          <div id="answer-area" style="display:none; margin-top:12px;">
            <label class="muted">Enter line number with the bug</label>
            <input id="chosen_line" name="chosen_line" type="number" min="1" autocomplete="off"/>
            <div style="margin-top:8px;" class="input">
              <button id="submit-btn" type="button" class="btn">Submit</button>
              <button id="giveup-btn" type="button" class="btn" onclick="location.href='{{ url_for('play') }}'">New Game</button>
            </div>
            <div id="msg" class="muted" style="margin-top:8px;"></div>
          </div>
        </form>
      </div>
      <div class="card">
        <div class="muted">Tips</div>
        <ul class="muted">
          <li>Look for missing colons, unmatched parentheses, indentation errors, wrong operators or wrong call syntax.</li>
          <li>Timer starts when you press <strong>Start</strong>.</li>
        </ul>
      </div>
    </aside>
  </div>
  
<script>
  const BUG_LINES = {{ bug['code']|tojson }};
  const ROLL_NO = {{ roll }};
  const CORRECT_LINE = {{ bug['correct_line'] }};

  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function renderCode(highlightIdx=null, revealAll=false){
    const codepre = document.getElementById('codepre');
    const gutter = document.getElementById('gutter');
    codepre.innerHTML = '';
    gutter.innerHTML = '';
    const kw_re = new RegExp('\\b(def|return|if|else|elif|for|in|while|import|from|class|try|except|with|pass|break|continue|print|True|False|None|and|or|not|lambda|raise)\\b','g');

    BUG_LINES.forEach((raw, i)=>{
      const ln = i+1;
      const gdiv = document.createElement('div');
      gdiv.textContent = ln;
      gdiv.style.padding = '2px 6px';
      gdiv.style.fontFamily = "'Fira Code', monospace";
      gdiv.style.color = 'var(--muted)';
      gutter.appendChild(gdiv);

      let line = esc(raw);
      line = line.replace(/(#.*$)/g, '<span class="cm">$1</span>');
      line = line.replace(/('[^']*'|"[^"]*")/g, '<span class="str">$1</span>');
      line = line.replace(/\b(\d+)\b/g, '<span class="num">$1</span>');
      line = line.replace(kw_re, '<span class="kw">$1</span>');
      line = line.replace(/([A-Za-z_][A-Za-z0-9_]*)\s*(?=\()/g, '<span class="fn">$1</span>');

      const lineWrap = document.createElement('div');
      lineWrap.className = 'line';
      lineWrap.innerHTML = line;
      if (highlightIdx !== null && ln === highlightIdx) {
        lineWrap.classList.add('highlight');
      }
      codepre.appendChild(lineWrap);
    });
  }
  renderCode();

  let timerInterval = null;
  const DURATION = 20;
  let timeLeft = DURATION;
  const timerEl = document.getElementById('timer');
  const startBtn = document.getElementById('start-btn');
  const answerArea = document.getElementById('answer-area');
  const chosenInput = document.getElementById('chosen_line');
  const submitBtn = document.getElementById('submit-btn');
  const msg = document.getElementById('msg');
  const correctHidden = document.getElementById('correct_line');

  function startRound(){
    answerArea.style.display = 'block';
    startBtn.disabled = true;
    renderCode();
    chosenInput.focus();
    timeLeft = DURATION;
    timerEl.textContent = timeLeft;
    timerInterval = setInterval(()=>{
      timeLeft--;
      timerEl.textContent = timeLeft;
      if (timeLeft <= 0){
        clearInterval(timerInterval);
        timerEl.textContent = 0;
        submitAnswer('');
      }
      if (timeLeft > 10) timerEl.style.color = '#28f73c';
      if (timeLeft > 5 && timeLeft < 11) timerEl.style.color = '#f56614';
      if (timeLeft <= 5) timerEl.style.color = '#a6020a';
    }, 1000);
  }

  function submitAnswer(choice){
    submitBtn.disabled = true;
    chosenInput.disabled = true;
    clearInterval(timerInterval);
    msg.textContent = 'Checking...';
    const form = document.createElement('form');
    form.method = 'post';
    form.action = "{{ url_for('result') }}";
    const add = (name, val) => {
      const i = document.createElement('input');
      i.type = 'hidden'; i.name = name; i.value = String(val);
      form.appendChild(i);
    };
    add('bug_idx', '{{ bug_idx }}');
    add('roll', '{{ roll }}');
    add('correct_line', CORRECT_LINE);
    add('chosen_line', choice);
    document.body.appendChild(form);
    form.submit();
  }

  startBtn.addEventListener('click', startRound);
  submitBtn.addEventListener('click', ()=>{
    const val = chosenInput.value ? chosenInput.value.trim() : '';
    if (val === ''){
      submitAnswer('');
    } else {
      submitAnswer(val);
    }
  });
</script>
</body>
</html>
"""

TEMPLATE_RESULT = r"""
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Bug Hunter — Result</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{ --bg:#0f1724; --panel:#0b1220; --muted:#9aa4b2; --accent:#ffca28; --text:#dbe7ef; --kw:#569cd6; --str:#98c379; --num:#d19a66; --cm:#6a737d; --fn:#dcdcaa; }
body{ margin:0; font-family:Inter, 'Fira Code', monospace; background:var(--bg); color:var(--text); }
.header{ padding:14px 22px; border-bottom:1px solid rgba(255,255,255,0.03); display:flex; justify-content:space-between; align-items:center; }
.logo{ background:linear-gradient(135deg,#2b333b,#0b1220); padding:8px 12px; border-radius:8px; color:var(--accent); font-weight:800; }
.container{ max-width:1100px; margin:20px auto; padding:18px; display:flex; gap:18px; align-items:flex-start; }
.ide{ flex:1; background:var(--panel); padding:12px; border-radius:12px; border:1px solid rgba(255,255,255,0.02); }
.codebox{ background:#0b1320; padding:12px; border-radius:8px; overflow:auto; max-height:520px; }
pre{ margin:0; font-family:'Fira Code','Courier New',monospace; font-size:14px; line-height:1.45; white-space:pre; }
.line{ display:block; padding:2px 6px; }
.kw{ color:var(--kw); font-weight:700; }
.str{ color:var(--str); }
.num{ color:var(--num); }
.cm{ color:var(--cm); font-style:italic; }
.fn{ color:var(--fn); }
.highlight{ background:rgba(255,77,79,0.12); border-left:4px solid rgba(255,77,79,0.9); border-radius:4px; padding-left:6px; }
.side{ width:320px; display:flex; flex-direction:column; gap:12px; }
.card{ background:linear-gradient(180deg,#06101a,#07111b); padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,0.02); }
.big{ font-size:28px; font-weight:800; color:var(--accent); }
.correct{ color:#8ce071; font-weight:800; font-size:18px; }
.wrong{ color:#ff6b6b; font-weight:800; font-size:18px; }
.expl{ margin-top:12px; color:var(--muted); }
.btn{ background:var(--accent); color:#071021; padding:8px 12px; border-radius:8px; border:none; font-weight:800; cursor:pointer; }
footer{ text-align:center; color:var(--muted); margin-top:20px; }

/* --- CSS for the bottom-right images --- */
.reaction-img {
    position: fixed;
    bottom: 0;
    right: 0;
    max-width: 300px;
    z-index: 9999;
    pointer-events: none;
}
@media (max-width:900px){ .container{ flex-direction:column; } .side{ width:100%; } }
</style>
</head>
<body>
  <div class="header">
    <div style="display:flex;gap:12px;align-items:center"><div class="logo">Bug Hunter</div><div style="font-weight:700">Result</div></div>
    <div class="muted">Player: <strong>{{ roll }}</strong></div>
  </div>

  <div class="container">
    <section class="ide">
      <div style="margin-bottom:12px;">
        {% if correct %}
          <div class="correct">✅ Correct!</div>
        {% else %}
          <div class="wrong">❌ Wrong.</div>
        {% endif %}
      </div>
      <div class="codebox">
        <pre id="codepre"></pre>
      </div>
      <div class="expl">
        <strong>Bug:</strong> {{ explanation }}
      </div>
    </section>

    <aside class="side">
      <div class="card">
        <div class="muted">Details</div>
        <div style="margin-top:8px;">
          <div class="muted">Correct line:</div>
          <div style="font-weight:800; margin-top:6px">{{ correct_line }}</div>
        </div>
        <div style="margin-top:12px;">
          <button class="btn" onclick="location.href='{{ url_for('play') }}'">New Game</button>
        </div>
      </div>
    </aside>
  </div>

  {% if correct %}
      <img src="{{ url_for('static', filename='abhi.png') }}" class="reaction-img" alt="Abhi">
  {% else %}
      <img src="{{ url_for('static', filename='sanjay.png') }}" class="reaction-img" alt="Sanjay">
  {% endif %}

  <footer>Hunt again! — Bug Hunter</footer>

<script>
  const LINES = {{ code_lines|tojson }};
  const HIGHLIGHT = {{ correct_line }};
  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  (function render(){
    const pre = document.getElementById('codepre');
    const kw_re = new RegExp('\\b(def|return|if|else|elif|for|in|while|import|from|class|try|except|with|pass|break|continue|print|True|False|None|and|or|not|lambda|raise)\\b','g');
    pre.innerHTML = '';
    LINES.forEach((raw, idx)=>{
      const ln = idx+1;
      let line = esc(raw);
      line = line.replace(/(#.*$)/g, '<span class="cm">$1</span>');
      line = line.replace(/('[^']*'|"[^"]*")/g, '<span class="str">$1</span>');
      line = line.replace(/\b(\d+)\b/g, '<span class="num">$1</span>');
      line = line.replace(kw_re, '<span class="kw">$1</span>');
      line = line.replace(/([A-Za-z_][A-Za-z0-9_]*)\s*(?=\()/g, '<span class="fn">$1</span>');
      const div = document.createElement('div');
      div.className = 'line';
      if (ln === HIGHLIGHT) div.classList.add('highlight');
      div.innerHTML = line;
      pre.appendChild(div);
    });
  })();
</script>
</body>
</html>
"""

# ------------------------
# Routes
# ------------------------
@app.route("/")
def home():
    return redirect(url_for('play'))

@app.route("/play")
def play():
    bug_idx = random.randrange(len(BUGS))
    roll = random.randint(1, 53)
    return render_template_string(TEMPLATE_READY, bug_idx=bug_idx, roll=roll)

@app.route("/question")
def question():
    bug_idx = request.args.get('bug_idx', None)
    roll = request.args.get('roll', None)
    if bug_idx is None or roll is None:
        return redirect(url_for('play'))
    try:
        bug_idx = int(bug_idx)
        roll = int(roll)
    except:
        return redirect(url_for('play'))
    if not (0 <= bug_idx < len(BUGS)):
        return redirect(url_for('play'))
    bug = BUGS[bug_idx]
    return render_template_string(TEMPLATE_QUESTION, bug=bug, bug_idx=bug_idx, roll=roll)

@app.route("/result", methods=["POST"])
def result():
    try:
        bug_idx = int(request.form.get('bug_idx', -1))
    except:
        return redirect(url_for('play'))
    try:
        roll = int(request.form.get('roll', 0))
    except:
        roll = 0
    bug = BUGS[bug_idx] if 0 <= bug_idx < len(BUGS) else None
    if bug is None:
        return redirect(url_for('play'))

    chosen = request.form.get('chosen_line', '').strip()
    try:
        chosen_i = int(chosen)
    except:
        chosen_i = None

    correct_line = bug['correct_line']
    is_correct = (chosen_i == correct_line)
    explanation = explain_bug(bug['code'], correct_line)

    return render_template_string(TEMPLATE_RESULT,
                                  correct=is_correct,
                                  code_lines=bug['code'],
                                  correct_line=correct_line,
                                  explanation=explanation,
                                  roll=roll)

if __name__ == "__main__":
    app.run(debug=True)