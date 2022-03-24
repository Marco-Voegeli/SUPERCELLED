import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:web_socket_channel/html.dart';
import 'package:web_socket_channel/io.dart';

void main() {
  runApp(const MyApp());
}

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
  bool connected = false;
  String myId = "";

  List<MessageData> msgList = [];
  TextEditingController msgtext = TextEditingController();

  @override
  void initState() {
    connected = false;
    msgtext.text = "";
    channelconnect();
    super.initState();
  }

  channelconnect() {
    //function to connect
    try {
      channel = HtmlWebSocketChannel.connect(Uri.parse('ws://10.15.7.28:8002'));
      channel.stream.listen(
        (message) {
          print(message);
          setState(() {
            if (message.toString().startsWith("connected")) {
              connected = true;
              myId = message.toString().split(" ")[1];
              setState(() {});
              print("Connection establised.");
              sendmsg("get_conv", myId, "cmd");
            } else {
              print("Message data");
              // message = message.replaceAll(RegExp("'"), '"');
              var jsondata = json.decode(message);

              var messages = jsondata["msgs"] as List<dynamic>;
              msgList = messages
                  .map((msg) => MessageData(
                      text: msg['text'],
                      userid: msg["userid"],
                      timestamp: msg["userid"]))
                  .toList();
              var otherUserEmotion = jsondata["emotions"];
              setState(() {
                //update UI after adding data to message model
              });
            }
          });
        },
        onDone: () {
          //if WebSocket is disconnected
          print("Web socket is closed");
          setState(() {
            connected = false;
          });
        },
        onError: (error) {
          print(error.toString());
        },
      );
    } catch (e) {
      print(e);
      print("error on connecting to websocket.");
    }
  }

  Future<void> sendmsg(String sendmsg, String id, String typ) async {
    if (connected == true) {
      String msg = json.encode({'userid': id, 'data': sendmsg, 'type': typ});
      setState(() {
        msgtext.text = "";
      });
      channel.sink.add(msg); //send message to reciever channel
    } else {
      channelconnect();
      print("Websocket is not connected.");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Group Chat"),
      ),
      body: connected
          ? Container(
              child: Stack(
              children: [
                Positioned(
                    top: 0,
                    bottom: 70,
                    left: 0,
                    right: 0,
                    child: Container(
                        padding: EdgeInsets.all(15),
                        child: SingleChildScrollView(
                            child: Column(
                          children: [
                            Container(
                              child: Text("Your Messages",
                                  style: TextStyle(fontSize: 20)),
                            ),
                            Container(
                                child: Column(
                                    // children: []msglist.map((onemsg){
                                    //   return Container(
                                    //      margin: EdgeInsets.only( //if is my message, then it has margin 40 at left
                                    //              left: onemsg.isme?40:0,
                                    //              right: onemsg.isme?0:40, //else margin at right
                                    //           ),
                                    //      child: Card(
                                    //         color: onemsg.isme?Colors.blue[100]:Colors.red[100],
                                    //         //if its my message then, blue background else red background
                                    //         child: Container(
                                    //           width: double.infinity,
                                    //           padding: EdgeInsets.all(15),

                                    //           child: Column(
                                    //             crossAxisAlignment: CrossAxisAlignment.start,
                                    //             children: [

                                    //               Container(
                                    //                 child:Text(onemsg.isme?"ID: ME":"ID: " + onemsg.userid)
                                    //               ),

                                    //               Container(
                                    //                  margin: EdgeInsets.only(top:10,bottom:10),
                                    //                  child: Text("Message: " + onemsg.msgtext, style: TextStyle(fontSize: 17)),
                                    //               ),

                                    //             ],),
                                    //         )
                                    //      )
                                    //   );
                                    // }).toList(),
                                    ))
                          ],
                        )))),
                Positioned(
                  //position text field at bottom of screen

                  bottom: 0, left: 0, right: 0,
                  child: Container(
                      color: Colors.black12,
                      height: 70,
                      child: Row(
                        children: [
                          Expanded(
                              child: Container(
                            margin: EdgeInsets.all(10),
                            child: TextField(
                              controller: msgtext,
                              decoration: InputDecoration(
                                  hintText: "Enter your Message"),
                            ),
                          )),
                          Container(
                              margin: EdgeInsets.all(10),
                              child: ElevatedButton(
                                child: Icon(Icons.send),
                                onPressed: () {
                                  if (msgtext.text != "") {
                                    // sendmsg(msgtext.text, recieverid); //send message with webspcket
                                  } else {
                                    print("Enter message");
                                  }
                                },
                              ))
                        ],
                      )),
                )
              ],
            ))
          : Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  Text(
                    'prout',
                    style: Theme.of(context).textTheme.headline4,
                  ),
                  TextButton(onPressed: channelconnect, child: Text("connect"))
                ],
              ),
            ),
    );
  }
}

class MessageData {
  //message data model
  String text, userid, timestamp;
  MessageData(
      {required this.text, required this.userid, required this.timestamp});
}
