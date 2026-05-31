#!/usr/bin/env python3
with open('C:\\Users\\Brittany\\AppData\\Local\\Temp\\opencode\\TuFish\\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add DexScreener adapter after Solana adapter, before MARKET LOADER
old = "// ===== MARKET LOADER ====="
new_adapter = """ADAPTERS.dexscreener = new (class extends BaseAdapter {
  constructor() { super({key:'dexscreener',label:'Memecoins',icon:'\U0001f32e',color:'#ff6b9d',badgeId:'badge-dex'}); }
  async fetchMarkets() {
    const memecoins = [
      {s:'BONK',n:'Bonk',a:'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'},
      {s:'WIF',n:'DogWifHat',a:'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm'},
      {s:'POPCAT',n:'Popcat',a:'7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr'},
      {s:'MEW',n:'cat in a dogs world',a:'MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5'},
      {s:'SAMO',n:'Samoyed Coin',a:'7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU'},
      {s:'MYRO',n:'Myro',a:'HhJpBhRRn4g56VsyLuT8DL5Bv31HkXqsrahTTUCZeZg4'},
      {s:'PENG',n:'Peng',a:'PENGuBnHr3UVfMi6T84B3r4qKpYFqh9hEw2JkfPfuVr'},
      {s:'BOME',n:'BOOK OF MEME',a:'ukHH6c7mMyiWCf1b9pnWe25TSpkDDt3H5pQZgZ74J82'},
      {s:'SILLY',n:'Silly Dragon',a:'7EYnhQoR9YM3N7UoaKRoA44Uy8JeaZV3RyouHeoBruuR'},
      {s:'MICHI',n:'Michi',a:'5B3Xx1RmXxJ6x3STgKvLTG6sPjjfhPL1Jd3yDbQWz3Pp'},
    ];
    try {
      const addresses = memecoins.map(t => t.a).join(',');
      const res = await fetch('https://api.dexscreener.com/latest/dex/tokens/' + memecoins.map(t => t.a).join(','), { signal: AbortSignal.timeout(8000) });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      const pairs = data.pairs || [];
      const bestPairs = {};
      pairs.forEach(p => {
        if (p.chainId !== 'solana') return;
        const addr = p.baseToken.address;
        if (!bestPairs[addr] || parseFloat(p.liquidity?.usd || 0) > parseFloat(bestPairs[addr].liquidity?.usd || 0)) {
          bestPairs[addr] = p;
        }
      });
      this.setBadge(true);
      return memecoins.map((t, i) => {
        const p = bestPairs[t.a];
        if (!p || !p.priceUsd) {
          return { id: 'dex_fb_' + i, question: t.s + ' ' + (Math.random() > 0.5 ? 'moon?' : 'dump?'), category: 'memecoins', adapter: 'dexscreener', yes_price: 0.5, volume: Math.floor(1e5 + Math.random() * 1e6), liquidity: Math.floor(1e4 + Math.random() * 5e5), change24h: (Math.random() - 0.5) * 30 };
        }
        const price = parseFloat(p.priceUsd);
        const vol = parseFloat(p.volume?.h24 || 0);
        const liq = parseFloat(p.liquidity?.usd || 0);
        const chg24 = parseFloat(p.priceChange?.h24 || 0);
        const fdv = parseFloat(p.fdv || 0);
        const prob = Math.min(0.95, Math.max(0.05, 0.5 + chg24 * 0.005));
        return {
          id: 'dex_' + t.s.toLowerCase(),
          question: t.s + ' ' + (chg24 >= 0 ? '>= $' : '<= $') + (price * (1 + Math.abs(chg24) * 0.005 + 0.05)).toFixed(8) + (i % 2 ? ' this week?' : ' today?'),
          category: 'memecoins', adapter: 'dexscreener',
          yes_price: prob, volume: vol, liquidity: liq,
          change24h: chg24, current_price: price, fdv: fdv,
        };
      });
    } catch {
      this.setBadge(false);
      return memecoins.map((t,i) => ({ id:'dex_fb_'+i, question:t.s+' '+(Math.random()>0.5?'pump?':'dump?'), category:'memecoins', adapter:'dexscreener', yes_price:0.4+Math.random()*0.3, volume:Math.floor(1e5+Math.random()*1e6), liquidity:Math.floor(1e4+Math.random()*5e5), change24h:(Math.random()-0.5)*30 }));
    }
  }
});

// ===== MARKET LOADER ====="""

c = c.replace(old, new_adapter, 1)
print("1. Adapter added")

# 2. Add badge in header
old_badge = '<div class="badge offline" id="badge-solana">SOL</div>'
new_badge = '<div class="badge offline" id="badge-solana">SOL</div>\n    <div class="badge offline" id="badge-dex">MEME</div>'
assert old_badge in c, "badge not found"
c = c.replace(old_badge, new_badge, 1)
print("2. Badge added")

# 3. Add source filter button
old_source = '<button class="qa-btn" onclick="filterSource(\'solana\',this)" style="font-size:8px;color:var(--solana-color)">SOL</button>'
new_source = '<button class="qa-btn" onclick="filterSource(\'solana\',this)" style="font-size:8px;color:var(--solana-color)">SOL</button>\n          <button class="qa-btn" onclick="filterSource(\'dexscreener\',this)" style="font-size:8px;color:var(--pink)">MEME</button>'
assert old_source in c, "source filter not found"
c = c.replace(old_source, new_source, 1)
print("3. Source filter added")

# 4. Add market category
old_cat = '<option value="solana">Solana</option>'
new_cat = '<option value="solana">Solana</option>\n              <option value="dexscreener">Memecoins</option>'
assert old_cat in c, "cat filter not found"
c = c.replace(old_cat, new_cat, 1)
print("4. Market category added")

# 5. Add sentiment category
emoji_sol = chr(0x25ce)
emoji_taco = chr(0x1f32e)
old_sent = "{id:'solana',name:'Solana',emoji:'" + emoji_sol + "'}"
new_sent = "{id:'solana',name:'Solana',emoji:'" + emoji_sol + "'},{id:'dexscreener',name:'Memecoins',emoji:'" + emoji_taco + "'}"
assert old_sent in c, "sentiment not found at " + str(c.find(old_sent))
c = c.replace(old_sent, new_sent, 1)
print("5. Sentiment category added")

# 6. Add to source defaults
old_sources = "sources:{polymarket:true,crypto:true,stocks:true,solana:true}"
new_sources = "sources:{polymarket:true,crypto:true,stocks:true,solana:true,dexscreener:true}"
assert old_sources in c, "sources not found"
c = c.replace(old_sources, new_sources, 1)
print("6. Source defaults updated")

# 7. Add CSS for memecoin source
old_css = ".mi-source.solana { background: rgba(0,255,136,0.15); color: var(--solana-color); }"
new_css = ".mi-source.solana { background: rgba(0,255,136,0.15); color: var(--solana-color); }\n.mi-source.dexscreener { background: rgba(255,107,157,0.15); color: var(--pink); }\n.sc-source.dexscreener { background: rgba(255,107,157,0.15); color: var(--pink); }"
assert old_css in c, "css not found"
c = c.replace(old_css, new_css, 1)
print("7. CSS added")

with open('C:\\Users\\Brittany\\AppData\\Local\\Temp\\opencode\\TuFish\\index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("\\nDone! File size:", len(c), "chars")
