import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const url = new URL(req.url).searchParams.get("url");
  if (!url || !/^https?:\/\//.test(url)) return NextResponse.json({ title: null }, { status: 400 });
  const html = await fetch(url, { headers: { "user-agent": "papert-lab-proto" } }).then((r) => r.text()).catch(() => "");
  const m = html.match(/<title[^>]*>([^<]{1,200})<\/title>/i);
  return NextResponse.json({ title: m ? m[1].trim() : null });
}
