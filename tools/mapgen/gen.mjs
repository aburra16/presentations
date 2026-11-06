import fs from 'fs';
import * as topojson from 'topojson-client';
import { geoConicEqualArea, geoPath, geoInterpolate, geoCentroid, geoBounds } from 'd3-geo';
const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/land-110m.json'));
const land = topojson.feature(topo, topo.objects.land);
const polys = land.features[0].geometry.coordinates.map(c=>({type:'Polygon',coordinates:c})).filter(p=>{const c=geoCentroid(p); const b=geoBounds(p); return c[0]<-30 && c[0]>-170 && c[1]>-58 && c[1]<70 && (b[1][0]-b[0][0])<200;});
const fc={type:'FeatureCollection',features:polys.map(g=>({type:'Feature',geometry:g}))};
const W=880,H=640;
const proj = geoConicEqualArea().parallels([-10,30]).rotate([78,0]).fitExtent([[10,10],[W-10,H-10]], fc).clipExtent([[0,0],[W,H]]);
const path = geoPath(proj);
const d = path(fc).replace(/(\d+\.\d)\d+/g,'$1');
const nyc=[-74.0,40.7], dst=[-55.0,-9.5];
const interp=geoInterpolate(nyc,dst);
const pts=[]; for(let i=0;i<=80;i++){const p=proj(interp(i/80)); pts.push([+p[0].toFixed(1),+p[1].toFixed(1)]);}
fs.writeFileSync('map.json', JSON.stringify({W,H,d,pts,nyc:proj(nyc).map(v=>+v.toFixed(1)),dst:proj(dst).map(v=>+v.toFixed(1))}));
console.log(polys.length, d.length, proj(nyc), proj(dst));
fs.writeFileSync('preview.html', `<body style="margin:0;background:#F2F3F0"><svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><path d="${d}" fill="#C8CAD2"/><polyline points="${pts.map(p=>p.join(',')).join(' ')}" fill="none" stroke="#7237FF" stroke-width="3" stroke-dasharray="1 9" stroke-linecap="round"/><circle cx="${proj(nyc)[0]}" cy="${proj(nyc)[1]}" r="6" fill="#7237FF"/><circle cx="${proj(dst)[0]}" cy="${proj(dst)[1]}" r="6" fill="#13D2E5"/></svg></body>`);
