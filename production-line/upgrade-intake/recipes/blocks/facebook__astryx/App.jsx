// 驗證用的真實區塊：商品列表區。
//
// 這不是 hello world。它刻意包含產線真正在用的元素：分類標籤、商品圖、
// 品名、售價、加入購物車按鈕、以及一個八件商品的網格。
// 目的是回答一個問題：這套設計系統能不能直接拿來做產線的商品區。
//
// 商品圖用內嵌 SVG，不連外部圖床。理由見 PITFALLS「熱連外部圖床，圖會消失」，
// 而且驗證不該因為別人的圖床掛掉而失敗。

import '@astryxdesign/core/reset.css';
import '@astryxdesign/core/astryx.css';
import '@astryxdesign/theme-neutral/theme.css';

import { Theme } from '@astryxdesign/core/theme';
import { neutralTheme } from '@astryxdesign/theme-neutral/built';
import { Card } from '@astryxdesign/core/Card';
import { Grid } from '@astryxdesign/core/Grid';
import { Button } from '@astryxdesign/core/Button';
import { Badge } from '@astryxdesign/core/Badge';
import { Heading, Text } from '@astryxdesign/core/Text';

const swatch = (hex) =>
  'data:image/svg+xml;utf8,' +
  encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">` +
      `<rect width="400" height="300" fill="${hex}"/>` +
      `<circle cx="200" cy="150" r="72" fill="rgba(255,255,255,0.35)"/>` +
    `</svg>`
  );

const PRODUCTS = [
  { id: 1, name: '亞麻寬版襯衫', desc: '透氣亞麻混紡，落肩剪裁', price: 1680, tag: '熱賣', hex: '#8a9a7b' },
  { id: 2, name: '純棉工裝褲', desc: '厚磅斜紋，四季可穿', price: 2280, tag: '補貨到', hex: '#6b7280' },
  { id: 3, name: '羊毛針織背心', desc: '美麗諾羊毛，不扎不刺', price: 1980, tag: '新品', hex: '#a1866f' },
  { id: 4, name: '皮革托特包', desc: '植鞣牛皮，越用越有味道', price: 3480, tag: '限量', hex: '#7c5c43' },
  { id: 5, name: '燈芯絨外套', desc: '寬版落肩，內裡舖棉', price: 3980, tag: '預購', hex: '#5f6b5a' },
  { id: 6, name: '帆布側背包', desc: '厚磅帆布，可放十四吋筆電', price: 1280, tag: '熱賣', hex: '#8f8878' },
  { id: 7, name: '水洗棉圓領衫', desc: '水洗處理，領口不變形', price: 880, tag: '基本款', hex: '#9aa0a6' },
  { id: 8, name: '羊毛混紡圍巾', desc: '雙面織紋，長度一百八十公分', price: 1180, tag: '季節限定', hex: '#7d6b7f' },
];

export default function App() {
  return (
    <Theme theme={neutralTheme}>
      <main style={{ maxWidth: 1200, margin: '0 auto', padding: '48px 24px' }}>
        <Heading level={1}>本季精選</Heading>
        <Text>
          以下八件商品由產線的商品資料直接產生，用來確認這套設計系統做得出可以賣東西的版面。
        </Text>
        <div style={{ height: 32 }} />
        <Grid columns={4} gap={4}>
          {PRODUCTS.map((p) => (
            <Card key={p.id} padding={4}>
              <img
                src={swatch(p.hex)}
                alt={p.name}
                width="100%"
                style={{ width: '100%', height: 'auto', borderRadius: 8, display: 'block' }}
              />
              <div style={{ height: 12 }} />
              <Badge label={p.tag} />
              <Heading level={3}>{p.name}</Heading>
              <Text size="sm">{p.desc}</Text>
              <div style={{ height: 8 }} />
              <Text>NT$ {p.price.toLocaleString('zh-Hant-TW')}</Text>
              <div style={{ height: 12 }} />
              <Button label={'把' + p.name + '加入購物車'} variant="primary">
                加入購物車
              </Button>
            </Card>
          ))}
        </Grid>
      </main>
    </Theme>
  );
}
