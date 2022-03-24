<<<<<<< HEAD
import React, { useState } from "react";

import "./App.css";
import gif from "./assets/happy.gif";


import firebase from "firebase/app";
import "firebase/firestore";
import "firebase/auth";
=======
import React, { useEffect, useState } from "react";
import "./App.css";
import "react-notifications-component/dist/theme.css";
// import gif from "./assets/angry.gif";
import { initializeApp } from "firebase/app";

import {
  getFirestore,
  collection,
  getDocs,
  deleteDoc,
  addDoc,
  serverTimestamp,
  where,
  orderBy,
  limit,
  query,
  onSnapshot,
} from "firebase/firestore";

import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import axios from "axios";
import { ReactNotifications, Store } from "react-notifications-component";
>>>>>>> 0195fe24ec27853e079cf5632ae389ee576de7c1

import { useAuthState } from "react-firebase-hooks/auth";

import { ChatMessageProps, Message } from "./types";
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDf6CO6CjkVutB9QvvSqpdIDycI6VNY-_s",
  authDomain: "chathack-f1679.firebaseapp.com",
  projectId: "chathack-f1679",
  storageBucket: "chathack-f1679.appspot.com",
  messagingSenderId: "845724221162",
  appId: "1:845724221162:web:45f074b2be6b8d69006193",
  measurementId: "G-QPN5ERN2JR",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

function SignIn() {
  const signInWithGoogle = async () => {
    const provider = new GoogleAuthProvider();
    const result = signInWithPopup(auth, provider);
  };
  return <button onClick={signInWithGoogle}>Sign in with Google</button>;
}

function SignOut() {
  return (
    auth.currentUser && <button onClick={() => auth.signOut()}>Sign Out</button>
  );
}

function ClearChat() {
  return (
    auth.currentUser && (
      <button
        onClick={async () => {
          const messagesRef = collection(db, "messages");

          const q = query(messagesRef, where("uid", "!=", "0"));
          const querySnapshot = await getDocs(q);
          querySnapshot.forEach((queryDoc) => {
            deleteDoc(queryDoc.ref);
          });
        }}
      >
        Clear Chat
      </button>
    )
  );
}

function ChatMessage(props: ChatMessageProps) {
  const { text, uid, photoURL } = props.message;
  const messageClass =
    auth.currentUser != null && uid === auth.currentUser.uid
      ? "sent"
      : "received";
  return (
    <div className={`message ${messageClass}`}>
<<<<<<< HEAD
=======
      {/* <img src={gif} alt="loading..." /> */}
>>>>>>> 0195fe24ec27853e079cf5632ae389ee576de7c1
      <img src={photoURL} />
      <p>{text}</p>
      <img src={gif} alt="loading..." />
    </div>
  );
}

function ChatRoom() {
  const messagesRef = collection(db, "messages");
  // const query = messagesRef.orderBy("createdAt").limit(25);
  const q = query(messagesRef, orderBy("createdAt"), limit(25));
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const unsubscibe = onSnapshot(q, (querySnapshot) => {
      const data = querySnapshot.docs.map((doc) => doc.data() as Message);
      setMessages(data);
    });
    return () => unsubscibe();
  }, []);

  const [formValue, setFormValue] = React.useState("");

  const dummy = React.useRef<HTMLDivElement>(null);

  const sendMessageToBackend = async () => {
    try {
      const resp = await axios.post("http://127.0.0.1:8000/get_emotions", {
        text: "fuck yourself",
      });
      console.log("GROS GROS PROUT");
      alert(JSON.stringify(resp.data));
    } catch (e) {
      console.log(e);
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    const user = auth && auth.currentUser && auth.currentUser;

    const uid = user && user.uid;
    const photoURL = user && user.photoURL;
    try {
      const docRef = await addDoc(collection(db, "messages"), {
        text: formValue,
        createdAt: serverTimestamp(),
        uid,
        photoURL,
      });
      console.log("Document written with ID: ", docRef.id);
    } catch (e) {
      console.log(e);
    }
    sendMessageToBackend();
    setFormValue("");
    dummy.current && dummy.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <>
      <main>
        {messages &&
          messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)}
        <div ref={dummy}></div>
      </main>
      <form onSubmit={sendMessage}>
        <input
          value={formValue}
          onChange={(e) => setFormValue(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </>
  );
}

function App() {
  const [user] = useAuthState(auth);
  return (
    <div className="App">
      <ReactNotifications />
      <header className="App-header">
        <h1>Chat App</h1>
        <ClearChat />
        <SignOut />
      </header>
      <section>{user ? <ChatRoom /> : <SignIn />}</section>
    </div>
  );
}



export default App;
