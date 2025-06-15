import tkinter as tk
import random
import math

# --- 定数設定 ---
# ウィンドウのサイズ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
# キャンバス（描画領域）のサイズ
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 550
# ニューロン（神経細胞）の数を増やして密度を調整
NUM_NEURONS = 150
# 脳の形状を定義する全体の半径
BRAIN_RADIUS_X = 280 # 単一の球体にするため調整
BRAIN_RADIUS_Y = 280 # Xと同じにして真円にする
# アニメーションの更新間隔（ミリ秒）
ANIMATION_INTERVAL = 50

class BrainFatigueVisualizer:
    """
    スマホ利用による脳疲労を可視化するアプリケーションのメインクラス
    """
    def __init__(self, root):
        self.root = root
        self.root.title("スマホ脳疲労シミュレーター")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # --- UI要素の作成 ---
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='#1a1a2e')
        self.canvas.pack()
        
        # 現在の状態を示すステータスラベルを追加
        self.status_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"))
        self.status_label.pack(pady=5)

        # ★★★ スライダーの最大値を8時間に変更 ★★★
        self.time_scale = tk.Scale(root, from_=0, to=8, resolution=0.1, orient=tk.HORIZONTAL,
                                   length=600, command=self.update_visualization)
        self.time_scale.set(0)
        self.time_scale.pack()

        # --- 脳ネットワークの初期化 ---
        self.neurons = []
        self.connections = []
        self.signals = []
        self.plaques = []
        # 各ニューロンの表示状態を管理
        self.visible_neurons = [True] * NUM_NEURONS

        self._setup_brain_network()
        self.update_visualization(0)
        self._animate_signals()

    def _setup_brain_network(self):
        """
        3D空間を意識して、球体内にニューロンを均等に配置する
        """
        center_x, center_y = CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2

        for i in range(NUM_NEURONS):
            angle = random.uniform(0, 2 * math.pi)
            sqrt_r = math.sqrt(random.uniform(0.0, 1.0))

            x = center_x + BRAIN_RADIUS_X * sqrt_r * math.cos(angle)
            y = center_y + BRAIN_RADIUS_Y * sqrt_r * math.sin(angle)
            
            self.neurons.append({
                'id': None, 'x': x, 'y': y,
                'r_base': random.uniform(3, 6),
                'z': random.uniform(-1, 1)
            })

        for i in range(NUM_NEURONS):
            for j in range(i + 1, NUM_NEURONS):
                p1 = self.neurons[i]
                p2 = self.neurons[j]
                dist_3d = math.hypot(p1['x'] - p2['x'],
                                      p1['y'] - p2['y'],
                                      (p1['z'] - p2['z']) * BRAIN_RADIUS_X)
                
                if dist_3d < 160 and random.random() < 0.18:
                    self.connections.append({'id': None, 'n1': i, 'n2': j})


    def update_visualization(self, value):
        """
        スライダーの値が変更されたときに呼び出され、全体の表示を更新する
        """
        usage_time = float(value)

        self.canvas.delete("all")

        self._draw_connections(usage_time)
        self._draw_neurons(usage_time)
        self._draw_plaques(usage_time)


    def _draw_neurons(self, usage_time):
        """
        現在の疲労度と奥行き(Z座標)に応じてニューロンを描画する
        """
        # ★★★ ニューロンの消滅が「2時間」から始まるように変更 ★★★
        self.visible_neurons = [True] * len(self.neurons)
        if usage_time > 2:
            # 2時間から8時間にかけて消滅確率が上がる
            disappear_prob = (usage_time - 2) / 6.0 * 0.7 
            for i in range(len(self.neurons)):
                 if random.random() < disappear_prob:
                    self.visible_neurons[i] = False
        
        drawable_neurons = []
        for i, neuron in enumerate(self.neurons):
            if self.visible_neurons[i]:
                drawable_neurons.append((i, neuron))
        
        drawable_neurons.sort(key=lambda item: item[1]['z'])

        for i, neuron in drawable_neurons:
            # ★★★ 疲労度の計算を「2時間」から始まるように変更 ★★★
            if usage_time < 2:
                fatigue = 0.0
            else:
                # 2時間から8時間にかけて疲労度が0から1に変化
                fatigue = min((usage_time - 2) / 6.0, 1.0) 

            z_factor = (neuron['z'] + 1) / 2
            display_r = neuron['r_base'] * (0.6 + z_factor * 0.8)
            brightness_mod = 0.8 + z_factor * 0.4

            r_healthy, g_healthy, b_healthy = 70, 180, 255
            r_fatigued, g_fatigued, b_fatigued = 80, 80, 90
            
            r = int((r_healthy * (1 - fatigue) + r_fatigued * fatigue) * brightness_mod)
            g = int((g_healthy * (1 - fatigue) + g_fatigued * fatigue) * brightness_mod)
            b = int((b_healthy * (1 - fatigue) + b_fatigued * fatigue) * brightness_mod)
            
            r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
            color = f'#{r:02x}{g:02x}{b:02x}'
            
            neuron['id'] = self.canvas.create_oval(
                neuron['x'] - display_r, neuron['y'] - display_r,
                neuron['x'] + display_r, neuron['y'] + display_r,
                fill=color, outline=color
            )

    def _draw_connections(self, usage_time):
        """
        現在の疲労度に応じてシナプス（接続）を描画する
        """
        if usage_time < 2:
            fatigue = 0.0
        else:
            fatigue = min((usage_time - 2) / 6.0, 1.0)
        
        width = max(2.5 * (1 - fatigue), 0.3)
        r_healthy, g_healthy, b_healthy = 100, 150, 220
        r_fatigued, g_fatigued, b_fatigued = 50, 50, 60
        r = int(r_healthy * (1 - fatigue) + r_fatigued * fatigue)
        g = int(g_healthy * (1 - fatigue) + g_fatigued * fatigue)
        b = int(b_healthy * (1 - fatigue) + b_fatigued * fatigue)
        color = f'#{r:02x}{g:02x}{b:02x}'

        for conn in self.connections:
            if self.visible_neurons[conn['n1']] and self.visible_neurons[conn['n2']]:
                n1 = self.neurons[conn['n1']]
                n2 = self.neurons[conn['n2']]
                conn['id'] = self.canvas.create_line(n1['x'], n1['y'], n2['x'], n2['y'], fill=color, width=width)

    def _draw_plaques(self, usage_time):
        """
        認知症フェーズで脳の老廃物（プラーク）を描画する
        """
        # ★★★ プラークの出現が「2時間」から始まるように変更 ★★★
        if usage_time > 2:
            # 2時間から8時間にかけてプラークの数が増える
            num_plaques = int((usage_time - 2) / 6.0 * (NUM_NEURONS * 0.4))
            
            if not self.plaques:
                center_x, center_y = CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2
                for _ in range(int(NUM_NEURONS * 0.4)):
                    angle = random.uniform(0, 2*math.pi)
                    sqrt_r = math.sqrt(random.uniform(0, 1))
                    px = center_x + BRAIN_RADIUS_X * sqrt_r * math.cos(angle)
                    py = center_y + BRAIN_RADIUS_Y * sqrt_r * math.sin(angle)
                    pr = random.uniform(3, 6)
                    self.plaques.append({'x': px, 'y': py, 'r': pr})
            
            for i in range(num_plaques):
                p = self.plaques[i]
                self.canvas.create_oval(p['x']-p['r'], p['y']-p['r'], p['x']+p['r'], p['y']+p['r'], 
                                        fill='#3d1e4d', outline='#3d1e4d')
        else:
            self.plaques = []


    def _animate_signals(self):
        """
        神経信号のアニメーションを処理する
        """
        if not self.connections: return

        usage_time = self.time_scale.get()
        if usage_time < 2:
            fatigue = 0.0
        else:
            fatigue = min((usage_time - 2) / 6.0, 1.0)
        
        visible_connections = [c for c in self.connections if self.visible_neurons[c['n1']] and self.visible_neurons[c['n2']]]
        
        if visible_connections and random.random() < 0.2 * (1 - fatigue * 0.9):
            conn = random.choice(visible_connections)
            signal = {
                'conn': conn,
                'progress': 0,
                'speed': random.uniform(0.02, 0.05) * (1 - fatigue * 0.8),
                'id': None
            }
            self.signals.append(signal)

        for signal in self.signals[:]:
            signal['progress'] += signal['speed']
            if signal['progress'] >= 1.0:
                self.canvas.delete(signal['id'])
                self.signals.remove(signal)
                continue
            
            conn_info = signal['conn']
            if self.visible_neurons[conn_info['n1']] and self.visible_neurons[conn_info['n2']]:
                n1 = self.neurons[conn_info['n1']]
                n2 = self.neurons[conn_info['n2']]
                x = n1['x'] + (n2['x'] - n1['x']) * signal['progress']
                y = n1['y'] + (n2['y'] - n1['y']) * signal['progress']
                
                if signal['id'] is not None:
                    self.canvas.delete(signal['id'])
                
                r = 3
                signal_color = "#f0e68c"
                signal['id'] = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=signal_color, outline=signal_color)
            else:
                self.canvas.delete(signal['id'])
                self.signals.remove(signal)

        self.root.after(ANIMATION_INTERVAL, self._animate_signals)


if __name__ == '__main__':
    root = tk.Tk()
    app = BrainFatigueVisualizer(root)
    root.mainloop()
