export interface Message {
    text: string,
    uid: string,
    photoURL: string,
    id: string
}

export type ChatMessageProps = {
    message: Message,
    key: string
}