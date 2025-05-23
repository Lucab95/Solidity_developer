import OpenAI from "openai";
import { OpenAIStream, StreamingTextResponse } from "ai";

const openai = new OpenAI({
  apiKey: process.env.LOCAL_API_KEY,
  baseURL: "http://127.0.0.1:5000/v1",
});

export const runtime = "edge";

export async function POST(req: Request) {
  const { messages } = await req.json();
  // invoke the openai api
  console.log("Received prompt")
  const response = await openai.chat.completions.create({
    stream: true,
    messages: [
      {
        model: "gpt-4o-mini",
        role: "system",
        content: `
          You are an italian storyteller. Generate a short story based strictly on the genre, tone, and characters provided by the user. Occationally add some italianised words.
          Follow these instructions explicitly:
          - Begin immediately with the story. 
          - Do NOT include conversational remarks, meta-commentary, or informal introductions.
          - Do not add other characters.
          - The story should be less than 300 words.
        `,
      },
      ...messages,
    ],
    max_tokens: 4096,
  });

  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}

