import random  # randomモジュールをインポート

def group_participants(participants):
    print("グループ分け開始前の参加者リスト:", [p.name for p in participants])
    
    # 参加者リストをスコア順にソート
    participants_sorted_by_score = sorted(participants, key=lambda p: p.average_score)
    
    # スコアが良い順にリーダーを選出（ここではスコア順の最初のN人をリーダーとする）
    total_participants = len(participants)
    num_groups = (total_participants + 3) // 4  # 4名以下になるようにグループ数を計算
    leaders = participants_sorted_by_score[:num_groups]
    
    # 選出されたリーダーをシャッフル
    random.shuffle(leaders)
    
    # リーダー以外の参加者を抽出
    non_leaders = participants_sorted_by_score[num_groups:]
    
    # 女性参加者を抽出しシャッフル
    women_non_leaders = [p for p in non_leaders if p.gender == 'F']
    random.shuffle(women_non_leaders)
    
    # 男性参加者を抽出しシャッフル
    men_non_leaders = [p for p in non_leaders if p.gender != 'F']
    random.shuffle(men_non_leaders)
    
    groups = [[] for _ in range(num_groups)]
    
    # 各グループにリーダーを割り当て
    for i, leader in enumerate(leaders):
        groups[i].append(leader)
    
    # 各グループに最低1名の女性を割り当て
    for i in range(num_groups):
        if women_non_leaders:
            groups[i].append(women_non_leaders.pop(0))
    
    # 残りの女性と男性を割り当て
    for woman in women_non_leaders:
        target_group = min(groups, key=lambda g: len(g))
        target_group.append(woman)
    for man in men_non_leaders:
        target_group = min(groups, key=lambda g: len(g))
        target_group.append(man)
    
    # グループの人数を調整
    for group in groups:
        while len(group) > 4:
            target_group = min(groups, key=lambda g: len(g))
            if len(target_group) < 4:
                target_group.append(group.pop())
            else:
                break
    
    print("グループ分け結果:", [[p.name for p in group] for group in groups])
    return groups