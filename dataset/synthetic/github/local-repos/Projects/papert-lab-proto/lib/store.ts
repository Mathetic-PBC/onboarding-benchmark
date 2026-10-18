"use client";
import { useSyncExternalStore } from "react";
import { nanoid } from "nanoid";

export type Source = { id: string; kind: "url" | "chat" | "cell" | "pdf"; title: string; ref: string; addedAt: string };
export type Cell = { id: string; text: string; createdAt: string; sources: string[] };  // source ids
export type Notebook = { id: string; title: string; cells: Cell[]; sources: Source[] };

const KEY = "papert:notebooks";
const listeners = new Set<() => void>();
const read = (): Notebook[] => JSON.parse(localStorage.getItem(KEY) || "[]");
const write = (nb: Notebook[]) => { localStorage.setItem(KEY, JSON.stringify(nb)); listeners.forEach((l) => l()); };

export const useNotebooks = () => useSyncExternalStore((l) => (listeners.add(l), () => listeners.delete(l)), read, () => []);
export const newNotebook = (title: string) => write([...read(), { id: nanoid(8), title, cells: [], sources: [] }]);
export const addCell = (nbId: string, text: string) =>
  write(read().map((n) => (n.id === nbId ? { ...n, cells: [...n.cells, { id: nanoid(8), text, createdAt: new Date().toISOString(), sources: [] }] } : n)));
export const linkSource = (nbId: string, cellId: string, src: Omit<Source, "id" | "addedAt">) =>
  write(read().map((n) => {
    if (n.id !== nbId) return n;
    const s = { ...src, id: nanoid(8), addedAt: new Date().toISOString() };
    return { ...n, sources: [...n.sources, s], cells: n.cells.map((c) => (c.id === cellId ? { ...c, sources: [...c.sources, s.id] } : c)) };
  }));
