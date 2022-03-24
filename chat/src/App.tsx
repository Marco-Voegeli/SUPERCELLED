import React, { useState } from "react";

import "./App.css";
import gif from "./assets/happy.gif";


import firebase from "firebase/app";
import "firebase/firestore";
import "firebase/auth";

import { useAuthState } from "react-firebase-hooks/auth";
import { useCollectionData } from "react-firebase-hooks/firestore";

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

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const firestore = firebase.firestore();

function SignIn() {
  const signInWithGoogle = () => {
    const provider = new firebase.auth.GoogleAuthProvider();
    auth.signInWithPopup(provider);
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
        onClick={() => {
          const messagesRef = firestore.collection("messages");
          messagesRef
            .where("uid", "!=", "0")
            .get()
            .then(function (query) {
              query.forEach(function (doc) {
                doc.ref.delete();
              });
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
      <img src={photoURL} />
      <p>{text}</p>
      <img src={gif} alt="loading..." />
    </div>
  );
}

function ChatRoom() {
  const messagesRef = firestore.collection("messages");
  const query = messagesRef.orderBy("createdAt").limit(25);

  const [messages]: [Message[] | undefined, boolean, Error | undefined] =
    useCollectionData<Message>(query, { idField: "id" });

  const [formValue, setFormValue] = React.useState("");

  const dummy = React.useRef<HTMLDivElement>(null);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    const user = auth && auth.currentUser && auth.currentUser;

    const uid = user && user.uid;
    const photoURL = user && user.photoURL;
    await messagesRef.add({
      text: formValue,
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
      uid,
      photoURL,
    });

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
