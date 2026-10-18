"use client";
import Link from "next/link";
import { useNotebooks, newNotebook } from "@/lib/store";

export default function Home() {
  const notebooks = useNotebooks();
  return (
    <main>
      <h1>Papert Lab</h1>
      <p>A notebook that remembers where your thoughts came from.</p>
      <button onClick={() => newNotebook("Untitled notebook")}>New notebook</button>
      <ul>{notebooks.map((n) => <li key={n.id}><Link href={`/notebook/${n.id}`}>{n.title}</Link> · {n.cells.length} cells</li>)}</ul>
    </main>
  );
}
