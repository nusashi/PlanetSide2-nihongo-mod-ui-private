# Python Cheat Sheet

## コーディングスタイル

*   **インデント**: スペース4つを使用します。タブは使用しません。
*   **1行の最大文字数**: 79文字を超えないようにします。長い行は、バックスラッシュ(`\`)を使って複数行に分割できます。
*   **命名規則**:
    *   関数名、変数名: スネークケース (例: `my_function`, `local_path`)
    *   クラス名: 大文字で始まるキャメルケース (例: `MyClass`, `ConfigManager`)
    *   定数: すべて大文字のスネークケース (例: `MAX_LENGTH`, `DEFAULT_VALUE`)
*   **型ヒント**: 変数や関数の引数、戻り値に型情報を付与します。
    ```python
    def greet(name: str) -> str:
        return f"Hello, {name}!"
    ```
*   **docstring**: 関数やクラスの শুরুতে、その機能や使い方を説明する文字列を記述します。
    ```python
    def add(x: int, y: int) -> int:
        """2つの数値を加算する

        Args:
            x (int): 1つ目の数値
            y (int): 2つ目の数値

        Returns:
            int: 加算結果
        """
        return x + y
    ```
*   **`if __name__ == '__main__':`ブロック**: スクリプトが直接実行された場合にのみ実行されるコードを記述します。
    ```python
    def main():
        print("This is the main function.")

    if __name__ == "__main__":
        main()
    ```

## 基本的な文法

### 変数

```python
# 変数への代入
x = 10
name = "Alice"
is_valid = True

# 型の確認
print(type(x))  # <class 'int'>
print(type(name))  # <class 'str'>
print(type(is_valid))  # <class 'bool'>
```

### データ型

*   **数値**: 整数 (`int`), 浮動小数点数 (`float`)
    ```python
    x = 10
    y = 3.14
    ```
*   **文字列**: (`str`)
    ```python
    name = "Alice"
    message = 'Hello, world!'
    ```
*   **リスト**: (`list`) 順序を持つ要素の集まり。変更可能。
    ```python
    numbers = [1, 2, 3, 4, 5]
    names = ["Alice", "Bob", "Charlie"]
    ```
*   **辞書**: (`dict`) キーと値のペアの集まり。変更可能。
    ```python
    person = {"name": "Alice", "age": 30, "city": "New York"}
    ```
*   **タプル**: (`tuple`) 順序を持つ要素の集まり。変更不可能（イミュータブル）。
    ```python
    coordinates = (10, 20)
    ```
*   **集合**: (`set`) 重複しない要素の集まり。
    ```python
    unique_numbers = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}  # {1, 2, 3, 4, 5}
    ```
*   **真偽値**: (`bool`) `True` または `False`
    ```python
    is_valid = True
    is_active = False
    ```

### 演算子

*   **算術演算子**: `+`, `-`, `*`, `/`, `//` (整数除算), `%` (剰余), `**` (べき乗)
*   **比較演算子**: `==`, `!=`, `>`, `<`, `>=`, `<=`
*   **論理演算子**: `and`, `or`, `not`
*   **代入演算子**: `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`
*   **ビット演算子**: `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (左シフト), `>>` (右シフト)

### 条件分岐

```python
x = 10

if x > 5:
    print("x is greater than 5")
elif x == 5:
    print("x is equal to 5")
else:
    print("x is less than 5")
```

### 繰り返し

```python
# forループ
for i in range(5):
    print(i)  # 0 1 2 3 4

# whileループ
count = 0
while count < 5:
    print(count)
    count += 1
```

### 関数定義

```python
def add(x: int, y: int) -> int:
    """2つの数値を加算する"""
    return x + y

result = add(3, 5)
print(result)  # 8
```

### クラス定義

```python
class Dog:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def bark(self):
        print("Woof!")

my_dog = Dog("Buddy", 3)
print(my_dog.name)  # Buddy
my_dog.bark()  # Woof!
```

## よく使う組み込み関数

*   `print()`: 出力
*   `input()`: 入力
*   `len()`: 長さ
*   `str()`: 文字列に変換
*   `int()`: 整数に変換
*   `float()`: 浮動小数点数に変換
*   `list()`: リストに変換
*   `dict()`: 辞書に変換
*   `range()`: 連続した整数のシーケンスを生成
*   `open()`: ファイルを開く

## モジュールのインポート

```python
# モジュール全体をインポート
import math

print(math.sqrt(16))  # 4.0

# モジュールから特定の関数やクラスをインポート
from math import sqrt

print(sqrt(16))  # 4.0

# モジュールに別名をつける
import math as m

print(m.sqrt(16))  # 4.0
```

## エラー処理

```python
try:
    x = int(input("Enter a number: "))
    result = 10 / x
    print(result)
except ValueError:
    print("Invalid input. Please enter a number.")
except ZeroDivisionError:
    print("Cannot divide by zero.")
finally:
    print("This will always be executed.")
```

## ファイル操作

```python
# ファイルの読み込み
with open("my_file.txt", "r") as f:
    contents = f.read()
    print(contents)

# ファイルの書き込み
with open("my_file.txt", "w") as f:
    f.write("Hello, world!")

# ファイルの追記
with open("my_file.txt", "a") as f:
    f.write("
This is a new line.")
```

## リスト内包表記、辞書内包表記

```python
# リスト内包表記
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]  # [1, 4, 9, 16, 25]

# 辞書内包表記
names = ["Alice", "Bob", "Charlie"]
name_lengths = {name: len(name) for name in names}  # {'Alice': 5, 'Bob': 3, 'Charlie': 7}
```

## f-string

```python
name = "Alice"
age = 30

message = f"My name is {name} and I am {age} years old."
print(message)  # My name is Alice and I am 30 years old.
```

## PySide6 (GUI)

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout()

label = QLabel("Hello, PySide6!")
layout.addWidget(label)

window.setLayout(layout)
window.show()

sys.exit(app.exec())
```

## コールバック、ボタン、無名関数

### コールバック関数

コールバック関数とは、あるイベントが発生したときに自動的に呼び出される関数のことです。PySide6では、ボタンがクリックされたとき、テキストが変更されたとき、ウィンドウが閉じられたときなど、さまざまなイベントが発生します。これらのイベントに対応する処理を記述するために、コールバック関数を使用します。

```python
# コールバック関数の例
def button_clicked():
    print("Button clicked!")
```

### ボタンへのコールバック関数の設定

PySide6でボタンにコールバック関数を設定するには、`QPushButton`の`clicked`シグナルにコールバック関数を接続します。

```python
import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout()

button = QPushButton("Click me!")

# 1. 通常の関数を接続する
def button_clicked():
    print("Button clicked!")

button.clicked.connect(button_clicked)

# 2. 無名関数（ラムダ式）を接続する
button.clicked.connect(lambda: print("Button clicked!"))

# 3. functools.partialを使用する
from functools import partial

def button_clicked_with_message(message):
    print(message)

button.clicked.connect(partial(button_clicked_with_message, "Button clicked!"))

layout.addWidget(button)
window.setLayout(layout)
window.show()

sys.exit(app.exec())
```

*   **通常の関数を接続する**: コールバック関数を定義し、`connect`メソッドにその関数を渡します。
*   **無名関数（ラムダ式）を接続する**: `lambda`キーワードを使って、その場で関数を定義し、`connect`メソッドに渡します。引数なしの簡単なコールバック関数を定義する場合に便利です。
*   **`functools.partial`を使用する**: `functools.partial`を使うと、関数の一部の引数を固定した新しい関数を作成できます。これを利用して、引数を持つコールバック関数をボタンに設定できます。

### 無名関数（ラムダ式）

ラムダ式は、名前を持たない小さな関数を定義するための構文です。`lambda`キーワードを使って定義します。

```python
# ラムダ式の構文
lambda arguments: expression

# ラムダ式の例
add = lambda x, y: x + y
result = add(3, 5)
print(result)  # 8
```

ラムダ式は、コールバック関数としてよく使用されます。

### functools.partial
`functools.partial`を使うと、既存の関数の一部の引数を固定化して、新しい関数を作成できます。

```python
from functools import partial

def greet(greeting, name):
  print(f"{greeting}, {name}!")

# greet関数のgreeting引数を"Hello"に固定
say_hello = partial(greet, "Hello")

say_hello("Alice") # Hello, Alice!
say_hello("Bob")   # Hello, Bob!
```

### より複雑なコールバック

#### 複数の関数を呼び出す

```python
def callback1():
    print("Callback 1")

def callback2():
    print("Callback 2")

def combined_callback():
    callback1()
    callback2()

button.clicked.connect(combined_callback)
```

#### 条件分岐を含む

```python
def conditional_callback():
    if button.isChecked():
        print("Button is checked")
    else:
        print("Button is not checked")

button.clicked.connect(conditional_callback)
```

#### クロージャを使う

```python
def outer_function(message):
    def inner_function():
        print(message)
    return inner_function

callback = outer_function("Hello from closure!")
button.clicked.connect(callback)  # "Hello from closure!"が出力される
```

#### クラスのメソッドをコールバック関数として使う

```python
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Click me!")
        self.button.clicked.connect(self.button_clicked) # selfに注意

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def button_clicked(self):
        print("Button clicked (from class method)!")
```

#### `@QtCore.Slot()` デコレータ (カスタムシグナル)
```python
from PySide6.QtCore import QObject, Signal, Slot

class MyObject(QObject):
    # カスタムシグナルを定義
    my_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def do_something(self):
        # シグナルを発行
        self.my_signal.emit("Something happened!")

class MyReceiver(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str)
    def handle_signal(self, message):
        # シグナルを受信したときの処理
        print(f"Received signal: {message}")

# オブジェクトを作成
sender = MyObject()
receiver = MyReceiver()

# シグナルとスロットを接続
sender.my_signal.connect(receiver.handle_signal)

# シグナルを発行
sender.do_something() # "Received signal: Something happened!" が出力される
```

## コメント

```python
# これは1行コメントです

"""
これは複数行の
コメントです
"""

# TODO: ここに後で実装するコードを記述する
```