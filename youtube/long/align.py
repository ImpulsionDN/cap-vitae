"""Aligne les phrases du texte sur les pauses détectées dans la voix (programmation dynamique)."""
import re, subprocess

def pauses(mp3, th=0.18):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', mp3, '-af', f'silencedetect=n=-35dB:d={th}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return [(float(e) - float(d) / 2, float(d)) for e, d in re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)', o)]

def sentences(par):
    return [s for s in re.split(r'(?<=[.!?:])\s+', par.strip()) if s]

def align(paras, mp3, D):
    """Renvoie pour chaque phrase (par paragraphe) son temps de fin."""
    sents = [(pi, s) for pi, p in enumerate(paras) for s in sentences(p)]
    ps = pauses(mp3) + [(D, 2.0)]
    lens = [len(s) + 4 for _, s in sents]; rate = D / sum(lens)
    N, P = len(sents), len(ps); INF = 1e18
    dp = [[INF] * P for _ in range(N)]; bk = [[-1] * P for _ in range(N)]
    for j in range(P):
        e = lens[0] * rate; got = ps[j][0]
        dp[0][j] = (got - e) ** 2 / max(e, 1) - 3 * ps[j][1]
    for i in range(1, N):
        e = lens[i] * rate
        for j in range(i, P):
            best, arg = INF, -1
            for k in range(max(0, j - 12), j):
                if dp[i - 1][k] >= INF: continue
                got = ps[j][0] - ps[k][0]
                c = dp[i - 1][k] + (got - e) ** 2 / max(e, 1)
                if c < best: best, arg = c, k
            if arg >= 0:
                bonus = 3 * ps[j][1] * (2.0 if sents[i][0] != (sents[i + 1][0] if i + 1 < N else -1) else 1.0)
                dp[i][j] = best - bonus; bk[i][j] = arg
    j = P - 1; ends = [0] * N
    for i in range(N - 1, -1, -1):
        ends[i] = ps[j][0]; j = bk[i][j]
    out = [[] for _ in paras]
    for (pi, s), t in zip(sents, ends): out[pi].append((s, t))
    return out
