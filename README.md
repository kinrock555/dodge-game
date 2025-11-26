# Dodge Game
Simple Pygame dodge game.


■避けゲー（ドッジゲーム）

■■設計
■プロジェクト名
・2D避けゲーv0.1

■使用技術
・言語；python
・ライブラリ；pygame
・NW環境；ローカル

■オブジェクト
・プレイヤー
	・位置(x,y)
	・大きさ(width,height)
	・速度(speed)
	・色(RGB)
・エネミー
	・位置(x,y)
	・大きさ(width,height)
	・速度(speed)
	・色(RGB)

・ゲーム状態
	・プレイステータス
	・開始時刻
	・生存時刻
・画面
	・画面サイズ
	・描写先
	・出力文字フォント


■フレーム
・ゲームにおける時間の単位(1秒の細分化)

・1フレーム
①キー入力(ボタン入力)
②キー入力チェック
③ゲーム状態の更新
④画面を描く
→最初に戻る(60FPSなら1秒間に60回繰り返す)

■座標
・構成
	・X:横(0→)
	・Y;縦(0↓)



■メモ
・pygame
	・pygame.time.Clock():時計オブジェクト
		・tick():フレームレートの設定
	・pygame.Rect(x, y, width, height):位置・大きさをまとめるオブジェクト
		・X.colliderec(Y)t：四角形のXとYが重なっている判定する関数(戻り値true,false)


	・pygame.key.get_pressed):キー入力管理オブジェクト
		・pygame.K_LEFT：左
	・pygame.draw：画面に図形を絵が食うための関数
    ・pygame.display.flip()：画面更新
・random.randint(最小値、最大値)：ランダム