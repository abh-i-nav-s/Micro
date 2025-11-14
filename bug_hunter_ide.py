# bug_hunter_ide.py
from flask import Flask, render_template_string, request, redirect, url_for
import random, html

app = Flask(__name__)

# -------------------------
# In-memory scoreboard (1..53)
# -------------------------
scores = {str(i): 0 for i in range(1, 54)}

# -------------------------
# 50 multi-line buggy snippets (each has "code": list-of-lines, "correct_line": int)
# Each snippet simulates a small Python function/loop with one mistake.
# -------------------------
bugs = [
    {
        "code": [
            "def greet(name)",
            "    if name:",
            "        print('Hello', name)",
            "    else:",
            "        print('No name')"
        ],
        "correct_line": 1
    },
    {
        "code": [
            "numbers = [1, 2, 3, 4]",
            "total = 0",
            "for i in numbers",
            "    total += i",
            "print(total)"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "def add(a, b):",
            "    return a + b",
            "",
            "print(add(5))"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "for i in range(3):",
            "print('Value:', i)",
            "    print('Done loop')"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "x = 10",
            "y = 0",
            "if y != 0:",
            "    print(x / y)",
            "else:",
            "    print('Cannot divide')"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "def find_max(nums):",
            "    max_num = nums[0]",
            "    for n in nums:",
            "        if n > max_num:",
            "        max_num = n",
            "    return max_num"
        ],
        "correct_line": 5
    },
    {
        "code": [
            "x = [1, 2, 3]",
            "for i in range(4):",
            "    print(x[i])",
            "print('Done')"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "def say_hello():",
            "    print('Hello')",
            "  print('Welcome!')",
            "say_hello()"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "for i in range(5)",
            "    print('Loop:', i)",
            "print('Finished')"
        ],
        "correct_line": 1
    },
    {
        "code": [
            "name = input('Enter name: ')",
            "if name = 'John':",
            "    print('Hi John!')",
            "else:",
            "    print('Not John')"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "def multiply(a, b):",
            "    result = a * b",
            "    return result",
            "print(result)"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "x = 5",
            "if x > 2",
            "    print('Big number')",
            "print('Done')"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "def greet_user(name):",
            "    print('Welcome, ' + name)",
            "greet_user()"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "items = ['pen', 'book', 'pencil']",
            "for item in items:",
            "print(item)",
            "print('End')"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "x = 10",
            "y = 5",
            "if x > y:",
            "print('x is greater')",
            "    print('Comparison done')"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "def check_even(num):",
            "    if num % 2 == 0:",
            "        print('Even')",
            "    else",
            "        print('Odd')"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "student = {'name': 'Raj', 'age': 20}",
            "print(student[name])"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "def divide(a, b):",
            "    if b == 0:",
            "        print('Cannot divide by zero')",
            "    else:",
            "        return a / b",
            "print(divide(5, 0)"
        ],
        "correct_line": 6
    },
    {
        "code": [
            "x = 3",
            "while x > 0:",
            "print(x)",
            "x -= 1"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "def get_area(radius):",
            "    area = 3.14 * radius ** 2",
            "    print('Area:', area)",
            "getarea(5)"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "for i in range(3):",
            "    for j in range(3):",
            "    print(i, j)",
            "print('Done')"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "def welcome(name):",
            "print('Hello', name)",
            "print('Done')"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "x = [1, 2, 3]",
            "print(x(0))",
            "print('ok')"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "for i in range(5):",
            "    if i == 3",
            "        print('Found 3')",
            "print('Loop Ended')"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "def factorial(n):",
            "    if n == 0:",
            "        return 1",
            "    else:",
            "        return n * factorial(n-1)",
            "print(factorial())"
        ],
        "correct_line": 6
    },
    {
        "code": [
            "x = 10",
            "y = 20",
            "if x > y:",
            "    print('X big')",
            "else:",
            "print('Y big')"
        ],
        "correct_line": 6
    },
    {
        "code": [
            "numbers = [10, 20, 30]",
            "for n in numbers",
            "    print(n)"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "def cube(x):",
            "    return x *** 3",
            "print(cube(2))"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "a = 5",
            "b = 0",
            "c = a / b",
            "print(c)"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "def sum_list(lst):",
            "    total = 0",
            "    for i in lst:",
            "        total = total + i",
            "    print(total)",
            "sum_list()"
        ],
        "correct_line": 6
    },
    {
        "code": [
            "for i in range(3):",
            "    for j in range(3):",
            "        print(i, j)",
            "    print('Inner loop done')",
            "print('Outer done')"
        ],
        "correct_line": 5
    },
    {
        "code": [
            "x = 5",
            "if x == 5:",
            "print('Correct')",
            "else:",
            "print('Wrong')"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "def hello():",
            "    print('Hello')",
            "print('Bye')",
            "Hello()"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "a = [1, 2, 3]",
            "for i in range(3):",
            "    print(a[i])",
            "print(a[3])"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "def add(a, b):",
            "    result = a + b",
            "return result"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "x = 10",
            "if x > 5:",
            "    print('Yes')",
            " else:",
            "    print('No')"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "def square(num):",
            "    result = num ** 2",
            "    return result",
            "print(result(5))"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "def main():",
            "    print('Start')",
            "if __name__ == '__main__'",
            "    main()"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "x = 1",
            "while x < 5:",
            "    print(x)",
            "x += 1"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "try:",
            "    print(10/0)",
            "except:",
            "print('Error')"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "def greet(msg='Hi')",
            "    print(msg)",
            "greet()"
        ],
        "correct_line": 1
    },
    {
        "code": [
            "x = int(input('Enter: '))",
            "if x % 2 == 0:",
            "    print('Even')",
            "else:",
            "print('Odd')"
        ],
        "correct_line": 5
    },
    {
        "code": [
            "def product(a, b):",
            "    return a * b",
            "print(product(a, b))"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "for i in range(3):",
            "    print('Value:', i)",
            "    if i == 1:",
            "    print('Middle')"
        ],
        "correct_line": 4
    },
    {
        "code": [
            "def display():",
            "print('Inside function')",
            "display()"
        ],
        "correct_line": 2
    },
    {
        "code": [
            "x = 5",
            "y = 10",
            "if x > y print('x greater')"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "def greet():",
            "    print('Hello')",
            "greet(",
            "print('Done')"
        ],
        "correct_line": 3
    },
    {
        "code": [
            "for i in range(2):",
            "    for j in range(2):",
            "        print(i,j)",
            "    print('Inner done')",
            "print('End'"
        ],
        "correct_line": 5
    },
]

# -------------------------
# Inline templates (single-file)
# -------------------------
TEMPLATE_BASE = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Bug Hunter IDE</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    /* Basic layout */
    :root{
      --bg:#0f1724;
      --panel:#0b1220;
      --muted:#9aa4b2;
      --accent:#ffca28;
      --ide-line:#0b1320;
      --keyword:#61afef;
      --string:#98c379;
      --number:#d19a66;
      --comment:#7f848a;
      --ident:#c678dd;
    }
    body{ margin:0;font-family:Inter, 'Fira Code', Menlo, monospace; background:var(--bg); color:#e6eef6; }
    header{ display:flex; align-items:center; justify-content:space-between; padding:14px 20px; background:linear-gradient(90deg,#071022, rgba(255,255,255,0.02)); border-bottom:1px solid rgba(255,255,255,0.03);}
    .brand{ display:flex; align-items:center; gap:12px; }
    .logo{ width:36px;height:36px; border-radius:6px; background:linear-gradient(135deg,#2b333b,#0b1220); display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--accent); box-shadow:0 6px 18px rgba(0,0,0,0.5);}
    h1{ font-size:18px;margin:0;}
    .controls{ display:flex; gap:8px; align-items:center;}
    .btn{ background:var(--accent); color:#071022; border:none; padding:8px 12px; border-radius:8px; cursor:pointer; font-weight:600; }
    .ghost{ background:transparent; color:var(--accent); border:1px solid rgba(255,255,255,0.04); padding:8px 10px; border-radius:8px; cursor:pointer;}
    main{ padding:20px; display:flex; gap:20px; align-items:flex-start; max-width:1100px; margin:18px auto;}
    /* IDE Panel */
    .ide { flex:1; background:var(--panel); border-radius:12px; padding:14px; box-shadow:0 8px 30px rgba(2,6,23,0.7); border:1px solid rgba(255,255,255,0.02);}
    .ide-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;}
    .tabs{ display:flex; gap:8px; align-items:center;}
    .tab { background:rgba(255,255,255,0.02); padding:6px 10px; border-radius:8px; color:var(--muted); font-size:13px;}
    .toolbar{ display:flex; gap:10px; align-items:center;}
    .timer { background:#071022; padding:6px 10px; border-radius:8px; border:1px solid rgba(255,255,255,0.02); color:var(--accent); font-weight:700;}
    /* Code area */
    .code-wrap{ display:flex; gap:12px; align-items:flex-start;}
    .gutter{ background:linear-gradient(180deg,rgba(255,255,255,0.01),transparent); padding:12px 8px; border-radius:8px; color:var(--muted); text-align:right; min-width:50px; }
    .codebox{ background:var(--ide-line); padding:12px; border-radius:8px; min-width:420px; max-width:100%; overflow:auto; box-shadow:inset 0 1px 0 rgba(255,255,255,0.02);}
    pre{ margin:0; font-family:'Fira Code', 'Courier New', monospace; font-size:14px; line-height:1.45; color:#dbe7ef; white-space:pre; }
    .line{ padding:2px 6px; display:block; min-width:600px; }
    /* Syntax colors (classes applied in JS) */
    .kw{ color:var(--keyword); font-weight:700; }
    .str{ color:var(--string); }
    .num{ color:var(--number); }
    .cm{ color:var(--comment); font-style:italic; }
    .ident{ color:var(--ident); }
    /* Right panel */
    .side { width:300px; display:flex; flex-direction:column; gap:12px; }
    .card { background:linear-gradient(180deg,#06101a,#07111b); padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,0.02); }
    .big { font-size:24px; font-weight:700; color:var(--accent); }
    .muted { color:var(--muted); font-size:13px; }
    label{ display:block; font-size:13px; margin-bottom:6px; color:var(--muted); }
    input[type=number]{ width:100%; padding:8px 10px; border-radius:8px; border:1px solid rgba(255,255,255,0.04); background:transparent; color:inherit; }
    .actions{ display:flex; gap:8px; margin-top:8px; }
    .score-table{ width:100%; border-collapse:collapse; color:#dbe7ef; font-size:13px; }
    .score-table th, .score-table td{ padding:6px 8px; border-bottom:1px solid rgba(255,255,255,0.02); text-align:left; }
    footer{ text-align:center; color:var(--muted); margin:20px 0 60px;}
    @media (max-width:900px){ main{ flex-direction:column; padding:12px; } .side{ width:100%; } .gutter{ display:none; } .codebox{ min-width:unset; } }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="logo">BH</div>
      <div>
        <h1>Bug Hunter — IDE Challenge</h1>
        <div class="muted">Find the buggy line within <strong>15 seconds</strong></div>
      </div>
    </div>
    <div class="controls">
      <a class="ghost" href="/">Home</a>
      <button class="btn" onclick="location.href='/scores'">View Scores</button>
    </div>
  </header>

  <main>
    <section class="ide card" aria-label="IDE">
      <div class="ide-top">
        <div class="tabs">
          <div class="tab">main.py</div>
          <div class="tab">utils.py</div>
        </div>
        <div class="toolbar">
          <div class="muted" id="roll-display">Roll: —</div>
          <div class="timer" id="timer">15</div>
        </div>
      </div>

      <div class="code-wrap">
        <div class="gutter" id="gutter"></div>
        <div class="codebox" id="codebox">
          <pre id="codepre">
{% for line in bug['code'] %}
<span class="line">{{ loop.index }}    {{ line|e }}</span>
{% endfor %}
          </pre>
        </div>
      </div>
    </section>

    <aside class="side">
      <div class="card">
        <div class="muted">Current Player</div>
        <div class="big" id="roll-big">{{ roll }}</div>
        <div style="margin-top:8px;">
          <form id="answer-form" method="post" action="/check">
            <input type="hidden" name="roll" value="{{ roll }}">
            <input type="hidden" name="correct_line" value="{{ bug['correct_line'] }}">
            <label for="chosen_line">Enter line number with bug</label>
            <input id="chosen_line" name="chosen_line" type="number" min="1" required autocomplete="off" />
            <div class="actions">
              <button id="submit-btn" type="submit" class="btn">Submit</button>
              <button id="next-btn" type="button" class="ghost" onclick="location.href='/play'">Skip / Next</button>
            </div>
            <div style="margin-top:8px;" class="muted">If timer reaches 0 the answer will be submitted automatically.</div>
          </form>
        </div>
      </div>

      <div class="card">
        <div class="muted">Quick Tips</div>
        <ul class="muted">
          <li>Look for missing colons, wrong indentation, wrong function calls, wrong variable names.</li>
          <li>Line numbers are shown left in the editor area.</li>
          <li>You have 15 seconds per round — be quick!</li>
        </ul>
      </div>

      <div class="card">
        <div class="muted">Small Leaderboard (top 6)</div>
        <table class="score-table" id="mini-scores">
          <thead><tr><th>Roll</th><th>Score</th></tr></thead>
          <tbody>
          {% for r,s in top_scores %}
            <tr><td>{{ r }}</td><td>{{ s }}</td></tr>
          {% endfor %}
          </tbody>
        </table>
      </div>
    </aside>
  </main>

  <footer>Made with ❤️ — Bug Hunter</footer>

  <script>
    // ====== Basic client-side syntax "highlighting" ======
    (function highlight(){
      const codepre = document.getElementById('codepre');
      if(!codepre) return;
      // Get the raw lines as array
      const lines = Array.from(codepre.querySelectorAll('.line'));
      // keywords, simple list
      const kw = ['def','return','if','else','elif','for','in','while','import','from','as','try','except','class','with','pass','break','continue','print','True','False','None','and','or','not','global','assert','yield','lambda','raise'];
      const kw_re = new RegExp('\\b(' + kw.join('|') + ')\\b', 'g');
      for (let el of lines){
        let text = el.textContent;
        // preserve leading numbers and spaces: remove the "index    " we've put in Jinja
        // the text format: "N    actual code"
        const idxMatch = text.match(/^(\d+)\s+(.*)$/s);
        if(!idxMatch) continue;
        const lineno = idxMatch[1];
        let code = idxMatch[2];
        // escape HTML
        code = code.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        // comments
        code = code.replace(/(#.*$)/g, '<span class="cm">$1</span>');
        // strings (single or double)
        code = code.replace(/('[^']*'|"[^"]*")/g, '<span class="str">$1</span>');
        // numbers
        code = code.replace(/\b(\d+)\b/g, '<span class="num">$1</span>');
        // keywords
        code = code.replace(kw_re, '<span class="kw">$1</span>');
        // simple function/identifier color (words that start with letter and contain letters/digits/_ and not already wrapped)
        // (skip inside spans)
        code = code.replace(/(^|[^A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)(?=[^A-Za-z0-9_]|$)/g, function(m, p1, p2){
          // don't color true/false/None which are keywords already handled
          const lower = p2;
          return p1 + '<span class="ident">'+p2+'</span>';
        });
        // put back the line with preserved line number left spacing for style
        el.innerHTML = '<strong style="color:var(--muted); margin-right:8px;">' + lineno + '</strong>' + code;
      }
    })();

    // ====== Timer logic (15s) ======
    (function timerLogic(){
      const DURATION = 15;
      let timeLeft = DURATION;
      const timerEl = document.getElementById('timer');
      const form = document.getElementById('answer-form');
      const chosenInput = document.getElementById('chosen_line');
      const submitBtn = document.getElementById('submit-btn');

      // Set initial focus and roll display
      const rollBig = document.getElementById('roll-big');
      const rd = rollBig ? rollBig.textContent.trim() : '';
      const rollDisplay = document.getElementById('roll-display');
      if(rollDisplay) rollDisplay.textCo
