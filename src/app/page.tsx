import ListComponents from "@/components/listcomponents";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-6xl w-full items-center justify-between text-sm lg:flex">
        <div className="w-full">
          <ListComponents />
        </div>
        <h2 className="text-4xl relative top-2 bg-[#E9E0D4] text-[#43766C] bg-opacity-10 p-8  rounded-lg shadow-lg">
          Tech Stack
          <ul className="text-lg list-disc space-y-3">
            <li>NextJS</li>
            <li>TailwindCSS</li>
            <li>FastAPI</li>
            <li>Swagger</li>
            <li>SQL Alchemy</li>
            <li>Neon Serverless(PostgresSQL)</li>
            <li>OAuth</li>
          </ul>
        </h2>
      </div>
    </main>
  );
}
