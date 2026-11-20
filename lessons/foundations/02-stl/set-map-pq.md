## เมื่อ vector ที่เรียงแล้วไม่พอ

บทที่แล้วเรา `sort` ครั้งเดียวแล้วถามด้วย `lower_bound` ได้สบาย แต่ถ้าข้อมูล **เปลี่ยนไปเรื่อย ๆ ระหว่างที่ถาม** ล่ะ เช่นมีของเข้า ของออก สลับกับคำถาม จะ `sort` ใหม่ทุกครั้งก็ $O(N \log N)$ ต่อครั้ง จะแทรกลง vector ที่เรียงไว้ก็ต้องเลื่อนข้อมูล $O(N)$ ต่อครั้ง พอมีเหตุการณ์เป็นแสนก็ TLE

บทนี้คือ container ที่ออกแบบมาให้ **แก้ไขได้เร็วและยังถามได้เร็ว**

| container | เก็บอะไร | งานหลัก |
|---|---|---|
| `set` / `multiset` | ค่าที่เรียงอยู่ตลอดเวลา | insert / erase / ค้นหา / `lower_bound` ใน $O(\log N)$ |
| `map` | คู่ key → value เรียงตาม key | นับความถี่, ผูกข้อมูลกับ key ใน $O(\log N)$ |
| `priority_queue` | ฮีป | หยิบตัวที่มากที่สุด (หรือน้อยที่สุด) ใน $O(\log N)$ |
| `deque` | อาเรย์ที่เปิดสองหัว | push / pop ได้ทั้งหน้าและหลังใน $O(1)$ |

## set และ multiset

`set<T>` เก็บค่า **ไม่ซ้ำ** และเรียงจากน้อยไปมากอยู่เสมอ ข้างในเป็น balanced binary search tree (red-black tree) ทุกงานหลักจึงเป็น $O(\log N)$ ส่วน `multiset<T>` เหมือนกันทุกอย่าง แต่เก็บค่าซ้ำได้

```cpp
set<int> s;
s.insert(5); s.insert(1); s.insert(5);   // s = {1, 5}  (5 ตัวที่สองไม่ถูกเพิ่ม)
s.erase(1);                              // ลบตามค่า
s.count(5);                              // 0 หรือ 1: มีหรือไม่มี
s.find(7) == s.end();                    // หาไม่เจอได้ end()
*s.begin();                              // ค่าน้อยสุด (ห้ามเรียกตอน s ว่าง)
*s.rbegin();                             // ค่ามากสุด
s.lower_bound(x);                        // ตัวแรกที่ >= x
s.upper_bound(x);                        // ตัวแรกที่ > x
for (int v : s) cout << v << ' ';        // วนได้ตามลำดับจากน้อยไปมาก
```

iterator ของ set ไม่ใช่ดัชนี บวกเลขตรง ๆ ไม่ได้ แต่เดินหน้าถอยหลังทีละก้าวได้ด้วย `next(it)` และ `prev(it)` ซึ่งเป็นท่าหลักเวลาอยาก "ดูเพื่อนบ้านซ้ายขวา" ของค่าหนึ่ง

### ตัวอย่างเต็ม: จองห้องพัก

โรงแรมมีห้องเลข $1$ ถึง $N$ ว่างทุกห้อง มีเหตุการณ์ $Q$ ครั้ง เหตุการณ์ `1 x` คือแขกขอห้อง **เลขน้อยที่สุดที่ไม่ต่ำกว่า $x$** ให้ตอบเลขห้องแล้วถือว่าห้องนั้นไม่ว่าง (ถ้าไม่มีตอบ $-1$) เหตุการณ์ `2 r` คือแขกคืนห้อง $r$

เก็บ **ห้องที่ยังว่าง** ไว้ใน set แล้วคำถามแต่ละข้อก็คือ `lower_bound` หนึ่งครั้ง

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  set<int> freeRooms;
  for (int r = 1; r <= n; r++) freeRooms.insert(r);

  while (q--) {
    int t, x;
    cin >> t >> x;
    if (t == 1) {
      auto it = freeRooms.lower_bound(x);   // ห้องว่างเลขแรกที่ >= x
      if (it == freeRooms.end()) {
        cout << -1 << '\n';
      } else {
        cout << *it << '\n';
        freeRooms.erase(it);                 // ลบด้วย iterator: ลบตัวนี้ตัวเดียว
      }
    } else {
      freeRooms.insert(x);                   // คืนห้อง
    }
  }
}
```

ทั้งโปรแกรมเป็น $O((N + Q) \log N)$ ถ้าใช้ vector ของห้องว่างแล้วไล่หาทีละห้อง จะเป็น $O(NQ)$

:::warning multiset::erase(ค่า) ลบทุกตัวที่เท่ากัน
`ms.erase(5)` บน `multiset` จะลบ 5 **ทุกตัว** ถ้าอยากลบแค่หนึ่งตัวให้ลบด้วย iterator:

```cpp
auto it = ms.find(5);
if (it != ms.end()) ms.erase(it);   // ลบ 5 ออกตัวเดียว
```

ถ้าเรียก `ms.erase(ms.find(5))` ตอนที่ไม่มี 5 อยู่เลย ก็จะเป็นการลบ `end()` ซึ่งเป็น undefined behaviour เช็กก่อนทุกครั้งถ้าโจทย์ไม่รับประกัน
:::

:::warning ใช้ s.lower_bound(x) ไม่ใช่ lower_bound(s.begin(), s.end(), x)
แบบหลังเป็นฟังก์ชันทั่วไปจาก `<algorithm>` ซึ่งกระโดดไปกลางช่วงไม่ได้เพราะ iterator ของ set ต้องเดินทีละก้าว ผลคือ $O(N)$ ต่อครั้ง คอมไพล์ผ่าน ได้คำตอบถูก แต่ TLE เงียบ ๆ ส่วน `s.lower_bound(x)` เป็นเมธอดของ set เองที่เดินลงต้นไม้ใน $O(\log N)$
:::

:::problem lp_stl05_nearest_van

:::hint ใบ้ Nearest Van
รถที่ใกล้ $x$ ที่สุดมีผู้สมัครแค่สองคัน คือคันแรกที่อยู่ที่ $\geq x$ (ได้จาก `lower_bound`) กับคันที่อยู่ก่อนหน้ามันหนึ่งตำแหน่ง (`prev`) ระวังสองกรณีขอบ: `lower_bound` ได้ `end()` และ `lower_bound` ได้ `begin()` ซึ่งไม่มีตัวก่อนหน้า ถ้าระยะเท่ากันให้เลือกคันที่อยู่ทางซ้าย ส่วนรถออกหนึ่งคันก็คือ `erase(find(x))` ไม่ใช่ `erase(x)`
:::

## map: ผูกค่ากับ key

`map<K, V>` เก็บคู่ `(key, value)` โดย key ไม่ซ้ำและเรียงอยู่เสมอ ข้างในเป็นต้นไม้แบบเดียวกับ set งานหลักจึง $O(\log N)$ เหมือนกัน การใช้งานที่เจอบ่อยที่สุดคือ **นับความถี่**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  int n;
  cin >> n;
  map<long long, int> cnt;
  for (int i = 0; i < n; i++) {
    long long x;
    cin >> x;
    cnt[x]++;                          // key ที่ยังไม่มีจะถูกสร้างด้วย value = 0 ก่อน
  }
  for (auto [value, times] : cnt)      // วนตาม key จากน้อยไปมาก
    cout << value << " x" << times << '\n';

  auto it = cnt.find(7);               // ถามว่ามี key นี้ไหม โดยไม่สร้างเพิ่ม
  cout << (it == cnt.end() ? 0 : it->second) << '\n';
}
```

ข้อดีเหนือการใช้อาเรย์นับคือ key จะใหญ่แค่ไหนก็ได้ (เช่น $10^{18}$) จะเป็นจำนวนติดลบ เป็น `string` หรือเป็น `pair` ก็ได้ ขอแค่เทียบด้วย `<` ได้

:::warning cnt[x] ตอน "แค่ถาม" ก็สร้าง key ใหม่
`if (cnt[x] > 0)` ดูเหมือนแค่อ่าน แต่ถ้ายังไม่มี `x` มันจะ **ใส่ `x` ลงไป** ด้วยค่า 0 ทำให้ map ใหญ่ขึ้นเรื่อย ๆ และ `cnt.size()` ผิด ถ้าแค่อยากรู้ว่ามีไหม ให้ใช้ `cnt.count(x)` หรือ `cnt.find(x)`
:::

:::problem lp_stl04_seen_before

:::hint ใบ้ Seen Before
ถ้าเก็บคำที่เคยเห็นใน vector แล้วไล่หาทุกครั้ง ก็ $O(N \cdot D)$ เมื่อ $D$ คือจำนวนคำที่ต่างกัน ซึ่งช้าเกินไปเมื่อคำแทบไม่ซ้ำกันเลย ให้ `map<string, int>` จำแทนว่าแต่ละคำเห็นมาแล้วกี่ครั้ง แล้วสังเกตว่า `++cnt[w]` คืนค่าหลังบวกแล้วให้ด้วย
:::

### แล้ว unordered_map ล่ะ

`unordered_map` (และ `unordered_set`) ใช้ hash table แทนต้นไม้ เฉลี่ยแล้ว $O(1)$ ต่อครั้ง แต่ **ไม่เรียง** และมีจุดอ่อน: hash ของจำนวนเต็มใน GCC คือค่าของมันเอง คนตั้งโจทย์ (หรือคน hack ใน Codeforces) จึงเตรียมชุดข้อมูลที่ทุกค่าตกช่องเดียวกันได้ ทำให้ทุกครั้งกลายเป็น $O(N)$ และทั้งโปรแกรมเป็น $O(N^2)$

คำแนะนำคือ **ใช้ `map` ไว้ก่อน** $O(\log N)$ ที่แน่นอนพอสำหรับเกือบทุกโจทย์ ถ้าจำเป็นต้องเร็วขึ้นจริง ๆ ให้ใส่ hash ที่สุ่มทุกครั้งที่รัน

```cpp
struct SafeHash {
  static unsigned long long splitmix64(unsigned long long x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
  }
  size_t operator()(unsigned long long x) const {
    static const unsigned long long seed = chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(x + seed);
  }
};

unordered_map<long long, int, SafeHash> cnt;   // ใช้เหมือน map ทุกอย่าง แต่ไม่เรียง
```

## priority_queue: หยิบตัวที่สำคัญที่สุดเสมอ

`priority_queue<T>` คือฮีป `top()` ดูตัวที่ **มากที่สุด** ใน $O(1)$ ส่วน `push` และ `pop` ใช้ $O(\log N)$ วนดูสมาชิกทั้งหมดไม่ได้ และลบตัวกลางไม่ได้ (ใครอยากรู้ไส้ในดูบท *Binary Heap Basics* ของแทร็ก Data Structures)

```cpp
priority_queue<int> mx;                                  // max-heap: top() คือค่ามากสุด
priority_queue<int, vector<int>, greater<int>> mn;       // min-heap: top() คือค่าน้อยสุด
priority_queue<pair<int, int>> pq;                       // pair: เทียบ first ก่อน แล้ว second
```

ค่าเริ่มต้นเป็น **max-heap** ซึ่งกลับด้านกับ `set` ที่ `begin()` เป็นตัวน้อยสุด จำง่าย ๆ ว่าใส่ `greater<T>` เมื่อต้องการตัวน้อยสุดอยู่บน อีกท่าที่ใช้กันบ่อยคือใส่ค่าติดลบเข้า max-heap แล้วกลับเครื่องหมายตอนหยิบออก

### ตัวอย่างเต็ม: ต่อเชือก

มีเชือก $N$ เส้น ต่อสองเส้นยาว $a$ กับ $b$ เสียค่าแรง $a + b$ และได้เชือกยาว $a + b$ ต้องการต่อจนเหลือเส้นเดียวโดยเสียค่าแรงรวมน้อยที่สุด

ทางที่ดีที่สุดคือ **ต่อสองเส้นที่สั้นที่สุดเสมอ** (เส้นสั้นถูกนับซ้ำหลายรอบ จึงควรอยู่ลึกที่สุด) งานนี้ต้องหยิบตัวน้อยสุดออกซ้ำ ๆ และใส่ค่าใหม่กลับ ซึ่งเป็นงานของ min-heap พอดี

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  int n;
  cin >> n;
  priority_queue<long long, vector<long long>, greater<long long>> pq;
  for (int i = 0; i < n; i++) {
    long long len;
    cin >> len;
    pq.push(len);
  }
  long long cost = 0;
  while (pq.size() > 1) {
    long long a = pq.top(); pq.pop();     // สั้นสุด
    long long b = pq.top(); pq.pop();     // สั้นรองลงมา
    cost += a + b;
    pq.push(a + b);
  }
  cout << cost << '\n';
}
```

เชือก `4 3 2 6` ต่อ $2 + 3 = 5$ แล้ว $4 + 5 = 9$ แล้ว $6 + 9 = 15$ รวม $29$ ทั้งหมด $N - 1$ รอบ รอบละ $O(\log N)$

:::problem lp_stl06_top_k_sum

:::hint ใบ้ Top K Prize
ไม่ต้องจำทุกคะแนน จำแค่ $K$ คะแนนที่ดีที่สุดก็พอ และคะแนนที่ "เสี่ยงหลุด" เมื่อมีคะแนนใหม่เข้ามาคือคะแนนที่ **น้อยที่สุด** ในกลุ่มนั้น ถามตัวเองว่าฮีปแบบไหนให้ดูตัวนั้นได้ใน $O(1)$ แล้วเก็บผลรวมของกลุ่มไว้เป็นตัวแปร ปรับทีละนิดแทนการบวกใหม่ทุกวัน คำตอบอาจถึงราว $5 \times 10^{15}$ ต้องใช้ `long long`
:::

## deque: เปิดได้สองหัว

`deque<T>` เหมือน vector ที่ `push_front` / `pop_front` ได้ใน $O(1)$ ด้วย และยังใช้ `dq[i]` ได้

```cpp
deque<int> dq;
dq.push_back(3);     // [3]
dq.push_front(1);    // [1, 3]
dq.push_back(7);     // [1, 3, 7]
dq.pop_front();      // [3, 7]
dq.front(); dq.back(); dq[1];   // 3, 7, 7
```

ถ้าใช้ `vector` แล้ว `erase(v.begin())` เพื่อเอาตัวหน้าออก จะเป็น $O(N)$ ทุกครั้ง ซึ่งเป็นสาเหตุ TLE ที่เจอบ่อยในโจทย์จำลองคิว `deque` (หรือ `queue` ซึ่งใช้ deque อยู่ข้างใน) แก้ตรงนี้ได้ทันที และจะได้ใช้ deque อีกเยอะในบท Sliding Window และ BFS

## เลือก container ยังไง

* ต้องการ **ค่าที่เรียงอยู่ตลอด** และหาเพื่อนบ้าน (ตัวที่ใกล้ที่สุด, ตัวแรกที่ $\geq x$) → `set` / `multiset`
* ต้องการ **นับ** หรือผูกข้อมูลกับ key ที่ใหญ่หรือไม่ใช่ตัวเลข → `map`
* ต้องการ **ตัวมากสุดหรือน้อยสุด** ซ้ำ ๆ อย่างเดียว → `priority_queue` (เร็วกว่า set ราวสองถึงสามเท่า)
* ต้องการเข้าออก **ที่หัวและท้าย** → `deque`
* ข้อมูลไม่เปลี่ยนหลังอ่านเสร็จ → `vector` + `sort` + `lower_bound` ยังเร็วที่สุด

## จุดที่พลาดบ่อย

* `*s.begin()`, `pq.top()`, `dq.front()` ตอนที่ container **ว่าง** คือ undefined behaviour เช็ก `empty()` ก่อน
* `prev(s.begin())` และ `*s.end()` ไม่มีอยู่จริง เวลาเดินหาเพื่อนบ้านต้องเช็กขอบทั้งสองด้าน
* ลบสมาชิกของ set ระหว่างวนลูป ให้ใช้ `it = s.erase(it);` เพราะ iterator ที่ถูกลบใช้ต่อไม่ได้
* `set` และ `map` มีค่าคงที่สูงกว่า vector มาก โดยเฉพาะบน judge ที่ไม่มี `-O2` ทำ $10^6$ ครั้งได้สบาย แต่ $10^7$ ครั้งเริ่มเสี่ยง

## สรุปสั้น ๆ

* `set` / `multiset` เรียงตลอดเวลา insert / erase / `lower_bound` ใน $O(\log N)$ ใช้เมธอด `s.lower_bound(x)` เสมอ
* ลบค่าเดียวจาก multiset ด้วย `ms.erase(ms.find(x))` ไม่ใช่ `ms.erase(x)`
* `map` นับความถี่ด้วย `cnt[x]++` แต่ถามว่ามีไหมด้วย `count` / `find` ใช้ `map` ก่อน `unordered_map` ถ้าไม่จำเป็น
* `priority_queue` เป็น max-heap ใส่ `greater<T>` เพื่อได้ min-heap
* `deque` push / pop ได้สองหัวใน $O(1)$ แทน `vector::erase(begin())` ที่เป็น $O(N)$
