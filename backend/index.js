import { exec } from "child_process";
import cors from "cors";
import dotenv from "dotenv";
import voice from "elevenlabs-node";
import express from "express";
import { promises as fs } from "fs";
import OpenAI from "openai";
dotenv.config();

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || "-", // Your OpenAI API key here, I used "-" to avoid errors when the key is not set but you should not do that
});

const elevenLabsApiKey = process.env.ELEVEN_LABS_API_KEY;
const voiceID = "21m00Tcm4TlvDq8ikWAM";

const app = express();
app.use(express.json());
app.use(cors());
const port = 3000;

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.get("/voices", async (req, res) => {
  res.send(await voice.getVoices(elevenLabsApiKey));
});

const execCommand = (command) => {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) reject(error);
      resolve(stdout);
    });
  });
};

const lipSyncMessage = async () => {
  const time = new Date().getTime();
  console.log(`Starting conversion for the message...`);
  await execCommand(
    `ffmpeg -y -i audios/output.mp3 audios/output.wav`
  );
  console.log(`Conversion done in ${new Date().getTime() - time}ms`);
  await execCommand(
    `/Users/srijanupadhyay/Projects/Ninjas/avatar/r3f-virtual-girlfriend-frontend/Rhubarb-Lip-Sync-1.13.0-macOS/rhubarb -f json -o audios/output.json audios/output.wav -r phonetic`
  );
  console.log(`Lip sync done in ${new Date().getTime() - time}ms`);
};

app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;
  // if (!userMessage) {
  //   res.send({
  //     messages: [
  //       {
  //         text: "Hey dear... How was your day?",
  //         audio: await audioFileToBase64("audios/intro_0.wav"),
  //         lipsync: await readJsonTranscript("audios/intro_0.json"),
  //         facialExpression: "smile",
  //         animation: "Talking_1",
  //       },
  //       {
  //         text: "I was really looking forward to see you today!!",
  //         audio: await audioFileToBase64("audios/intro_1.wav"),
  //         lipsync: await readJsonTranscript("audios/intro_1.json"),
  //         facialExpression: "smile",
  //         animation: "Talking_1",
  //       },
  //     ],
  //   });
  //   return;
  // }
  
  // const completion = await openai.chat.completions.create({
  //   model: "gpt-3.5-turbo-1106",
  //   max_tokens: 1000,
  //   temperature: 0.9,
  //   response_format: {
  //     type: "json_object",
  //   },
  //   messages: [
  //     {
  //       role: "system",
  //       content: `
  //       You are an AI Assistant that is supposed to behave like my friend. Give me a reply using slang, which makes you seem like a friend instead of a machine.
  //       You will always reply with a JSON array of messages.
  //       Each message has a text.
  //       `,
  //     },
  //     {
  //       role: "user",
  //       content: userMessage || "Hello",
  //     },
  //   ],
  // });

  // let messages = JSON.parse(completion.choices[0].message.content);
  // if (messages.messages) {
  //   messages = messages.messages;
  // }
  // console.log(messages)

  if (!userMessage) {
    const message = {
      text: "Playing output.mp3",
      facialExpression: "smile",
      animation: "Talking_1",
    };
  
    // Generate lip-sync data
    await lipSyncMessage();
    message.audio = await audioFileToBase64("audios/output.mp3");
    message.lipsync = await readJsonTranscript("audios/output.json");
  
    res.send({ messages: [message] });
  }
  //  else {
  //   res.send({
  //     messages: [
  //       {
  //         text: "Hey dear... How was your day?",
  //         audio: await audioFileToBase64("audios/intro_0.wav"),
  //         lipsync: await readJsonTranscript("audios/intro_0.json"),
  //         facialExpression: "smile",
  //         animation: "Talking_1",
  //       },
  //       {
  //         text: "I was really looking forward to see you today!!",
  //         audio: await audioFileToBase64("audios/intro_1.wav"),
  //         lipsync: await readJsonTranscript("audios/intro_1.json"),
  //         facialExpression: "smile",
  //         animation: "Talking_1",
  //       },
  //     ],
  //   });
  // }



  // for (let i = 0; i < messages.length; i++) {
  //   const message = messages[i];
  //   // generate audio file
  //   const fileName = `audios/output.mp3`; // The name of your audio file
  //   // generate lipsync
  //   await lipSyncMessage(i);
  //   message.audio = await audioFileToBase64(fileName);
  //   message.lipsync = await readJsonTranscript(`audios/output.json`);
  // }


  // for (let i = 0; i < messages.length; i++) {
  //   const message = messages[i];
  //   // generate audio file
  //   const fileName = `audios/message_${i}.mp3`; // The name of your audio file
  //   const textInput = message.text; // The text you wish to convert to speech
  //   await voice.textToSpeech(elevenLabsApiKey, voiceID, fileName, textInput);
  //   // generate lipsync
  //   await lipSyncMessage(i);
  //   message.audio = await audioFileToBase64(fileName);
  //   message.lipsync = await readJsonTranscript(`audios/message_${i}.json`);
  // }

  // res.send({ messages });
});

const readJsonTranscript = async (file) => {
  const data = await fs.readFile(file, "utf8");
  return JSON.parse(data);
};

const audioFileToBase64 = async (file) => {
  const data = await fs.readFile(file);
  return data.toString("base64");
};


app.post("/execute-command", (req, res) => {
  exec('python3 app.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).send({ error: `exec error: ${error}` });
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
    const responseData = { output: stdout };
    console.log('Response data:', responseData); // Add this line
    res.send(responseData);
  });
});

app.listen(port, () => {
  console.log(`Virtual Assistant listening on port ${port}`);
});
