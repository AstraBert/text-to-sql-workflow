"use client"

import { ApiProvider } from "@llamaindex/ui";
import RunButton from "@/components/base";
import { clients } from "@/lib/clients"

export default function Home() {
  return (
    <div>
      <ApiProvider clients={clients}>
        <RunButton />
      </ApiProvider>
    </div>
  );
}
