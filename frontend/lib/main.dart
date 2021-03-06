import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:web_socket_channel/html.dart';
import 'package:loading_indicator/loading_indicator.dart';

void main() {
  runApp(const MyApp());
}

const List<Color> _kDefaultRainbowColors = [
  Colors.red,
  Colors.orange,
  Colors.yellow,
  Colors.green,
  Colors.blue,
  Colors.indigo,
  Colors.purple,
];
const equi = {"0": "A", "1": "B"};
const other_equi = {"0": "B", "1": "A"};

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Empathy',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: const ChatPage(),
    );
  }
}

class ChatPage extends StatefulWidget {
  const ChatPage({Key? key}) : super(key: key);

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  late HtmlWebSocketChannel channel;
  int connected = 0;
  String myId = "";
  String otherUserEmotion = "";
  List<MessageData> msgList = [];
  TextEditingController msgtext = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  late FocusNode myFocusNode;
  bool waitingForModel = true;
  String rawModelData = "";
  String gif_url = "";

  @override
  void initState() {
    msgtext.text = "";
    myFocusNode = FocusNode();
    channelconnect();
    super.initState();
    WidgetsBinding.instance?.addPostFrameCallback((_) =>
        _scrollController.jumpTo(_scrollController.position.maxScrollExtent));
  }

  channelconnect() {
    //function to connect
    try {
      channel = HtmlWebSocketChannel.connect(Uri.parse('ws://localhost:8002'));
      channel.stream.listen(
        (message) {
          try {
            if (message.toString().startsWith("connected")) {
              connected = 1;
              myId = message.toString().split(" ")[1];
              setState(() {});
              print("Connection establised.");
              sendmsg("get_conv", myId, "cmd");
            } else {
              // print("Message data");
              // message = message.replaceAll(RegExp("'"), '"');
              var jsondata = json.decode(message);
              if (jsondata["msgs"] != null) {
                var messages = jsondata["msgs"] as List<dynamic>;
                print("Received messages " + messages.length.toString());
                msgList = messages
                    .map((msg) => MessageData(
                        text: msg['text'],
                        userid: msg["userid"],
                        timestamp: msg["userid"]))
                    .toList();
                waitingForModel = true;
                setState(() {});
              } else if (jsondata["emotions"] != null) {
                print("Received emotions: " + jsondata["emotions"].toString());
                rawModelData = jsondata["emotions"].toString();
                waitingForModel = false;
                String tmp = jsondata["emotions"][myId == "0" ? 1 : 0];
                otherUserEmotion = tmp.split(" ").last;
                gif_url = jsondata[(myId == "0" ? "B" : "A") + "_gif_url"];
                setState(() {});
              }
            }
          } catch (e) {
            print(e);
          }
          //update UI after adding data to message model
        },
        onDone: () {
          //if WebSocket is disconnected
          print("Web socket is closed");
          setState(() {
            // connected = false;
          });
        },
        onError: (error) {
          print("The error is here");
          print(error.toString());
        },
        cancelOnError: true,
      );
    } catch (e) {
      print(e);
      print("error on connecting to websocket.");
    }
  }

  Future<void> sendmsg(String sendmsg, String id, String typ) async {
    if (connected == 1) {
      String msg = json.encode({'userid': id, 'data': sendmsg, 'type': typ});
      setState(() {
        msgtext.text = "";
      });
      waitingForModel = true;
      channel.sink.add(msg);
      //send message to reciever channel
      setState(() {});
    } else if (connected == 0) {
      channelconnect();
      print("Websocket is not connected.");
    } else {}
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Group Chat" +
              (equi[myId] == null ? "" : " - User " + (equi[myId] ?? "")),
          style: const TextStyle(fontSize: 20),
        ),
        actions: [
          IconButton(
            onPressed: () => sendmsg("clear", myId, "cmd"),
            icon: const Icon(Icons.restore_outlined),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.send),
        onPressed: () {
          if (msgtext.text != "") {
            sendmsg(msgtext.text, myId, "txt");
          }
        },
      ),
      body: connected == 1
          ? Column(
              children: [
                Expanded(
                  flex: 12,
                  child: Container(
                    padding: const EdgeInsets.all(15),
                    child: Column(
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        Expanded(
                          flex: 2,
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            children: [
                              Column(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceEvenly,
                                mainAxisSize: MainAxisSize.max,
                                children: [
                                  const Padding(
                                    padding: EdgeInsets.only(bottom: 20),
                                    child: Text(
                                      "Raw data of the assistant :",
                                      style: TextStyle(
                                          fontSize: 15,
                                          fontWeight: FontWeight.bold),
                                    ),
                                  ),
                                  waitingForModel
                                      ? const Padding(
                                          padding: EdgeInsets.all(8.0),
                                          child: SizedBox(
                                            width: 80,
                                            height: 80,
                                            child: LoadingIndicator(
                                              indicatorType: Indicator
                                                  .ballTrianglePathColoredFilled,
                                              colors: _kDefaultRainbowColors,
                                              strokeWidth: 4.0,
                                            ),
                                          ),
                                        )
                                      : Text(rawModelData)
                                ],
                              ),
                              Column(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceEvenly,
                                mainAxisSize: MainAxisSize.max,
                                children: [
                                  gif_url != ""
                                      ? Container(
                                          // clipBehavior: ,
                                          width: size.width * 0.2,
                                          child: Image.network(gif_url))
                                      : const SizedBox.shrink(),
                                  const SizedBox(
                                    height: 20,
                                  ),
                                  Text("User " +
                                      (other_equi[myId] ?? "undef") +
                                      " is feeling " +
                                      otherUserEmotion),
                                ],
                              ),
                            ],
                          ),
                        ),
                        const Divider(
                          color: Colors.grey,
                          thickness: 2,
                        ),
                        Expanded(
                          flex: 3,
                          child: ListView.builder(
                            shrinkWrap: true,
                            controller: _scrollController,
                            itemCount: msgList.length,
                            itemBuilder: (context, idx) {
                              if (idx == msgList.length - 1) {
                                Future.delayed(
                                    const Duration(milliseconds: 100),
                                    () => _scrollController.animateTo(
                                        _scrollController
                                            .position.maxScrollExtent,
                                        duration:
                                            const Duration(milliseconds: 200),
                                        curve: Curves.easeIn));
                              }
                              final onemsg = msgList[idx];
                              var isMe = onemsg.userid == myId;
                              return Container(
                                padding: EdgeInsets.only(
                                  //if is my message, then it has margin 40 at left
                                  left: isMe ? size.width * 0.4 : 0,
                                  right: isMe
                                      ? 0
                                      : size.width * 0.4, //else margin at right
                                ),
                                child: Card(
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(15.0),
                                  ),
                                  color:
                                      isMe ? Colors.blue[100] : Colors.red[100],
                                  //if its my message then, blue background else red background
                                  child: Container(
                                    width: MediaQuery.of(context).size.width *
                                        0.60,
                                    padding: const EdgeInsets.all(15),
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(isMe
                                            ? "ID: ME"
                                            : "ID: " + onemsg.userid),
                                        Container(
                                          margin: const EdgeInsets.only(
                                              top: 10, bottom: 10),
                                          child: Text("Message: " + onemsg.text,
                                              style: const TextStyle(
                                                  fontSize: 17)),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                Expanded(
                  flex: 2,
                  child: Row(
                    children: [
                      Expanded(
                          child: Container(
                        decoration: const BoxDecoration(
                            // border: Border.all(color: Colors.black, ),
                            borderRadius: BorderRadius.all(Radius.circular(20)),
                            color: Color.fromARGB(255, 211, 211, 211)),
                        margin: const EdgeInsets.only(
                            bottom: 0, right: 40, left: 10),
                        child: Padding(
                          padding: const EdgeInsets.all(15),
                          child: Container(
                            height: 50,
                            child: TextField(
                              autofocus: true,
                              focusNode: myFocusNode,
                              onSubmitted: (value) {
                                sendmsg(value, myId, "txt");
                                msgtext.clear();
                                myFocusNode.requestFocus();
                              },
                              controller: msgtext,
                              decoration: const InputDecoration.collapsed(
                                  hintText: "Enter your Message"),
                            ),
                          ),
                        ),
                      ))
                    ],
                  ),
                ),
              ],
            )
          : (connected == 0
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: <Widget>[
                      const CircularProgressIndicator(),
                      TextButton(
                          onPressed: channelconnect,
                          child: const Text("connect"))
                    ],
                  ),
                )
              : Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: const <Widget>[
                      Text("Error while parsing message")
                    ],
                  ),
                )),
    );
  }
}

class MessageData {
  //message data model
  String text, userid, timestamp;
  MessageData(
      {required this.text, required this.userid, required this.timestamp});
}
