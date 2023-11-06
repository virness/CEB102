import 'package:path_provider/path_provider.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/services.dart';
import 'package:video_player/video_player.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:permission_handler/permission_handler.dart';
import 'package:vibration/vibration.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';
void main() {
  runApp(MyApp());
}
Future<String> fetchGPT3Response(String prompt) async {
  final apiKey = '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';
  // final url = 'https://api.openai.com/v1/chat/completions';
  final url = '';
  final headers = {
    'Authorization': 'Bearer $apiKey',
    'Content-Type': 'application/json',
  };
  final body = jsonEncode({
    'model': 'gpt-3.5-turbo',
    'messages': [
      {'role': 'system', 'content': 'You are a helpful assistant.'},
      {'role': 'user', 'content': prompt}
    ]
  });
  final response = await http.post(
    Uri.parse(url),
    headers: headers,
    body: body,
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return data['choices'][0]['message']['content'];
  } else {
    return 'Failed to fetch GPT-3.5 Turbo response: ${response.body}';
  }
}
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MSNStyleChat(), // 修改這裡，使用 MSNStyleChat 作為首頁
    );
  }
}
class ChatPage extends StatefulWidget {
final String friendName;

ChatPage({required this.friendName});

@override
_ChatPageState createState() => _ChatPageState();
}
class _ChatPageState extends State<ChatPage> {
final TextEditingController _messageController = TextEditingController();
List<Map<String, dynamic>> messages = []; // 在這裡初始化 messages
@override // 注意這裡，你缺失了這個部分
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(
      title: Text('Chat with ${widget.friendName}'),
    ),
    body: Column(
      children: [
        Expanded(
          child: ListView.builder(
            itemCount: messages.length,
            itemBuilder: (context, index) {
              final message = messages[index];
              // 在這裡添加用於顯示訊息的代碼
            },
          ),
        ),
        Container(
          padding: EdgeInsets.all(8.0),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _messageController,
                  decoration: InputDecoration(
                    hintText: "Enter message...",
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
              IconButton(
                icon: Icon(Icons.send),
                onPressed: () {
                  String newMessage = _messageController.text;
                  if (newMessage.isNotEmpty) {
                    setState(() {
                      messages.add({
                        'sender': 'You',
                        'content': newMessage,
                        'time': DateFormat('hh:mm a').format(DateTime.now()),
                        'type': 'text',
                      });
                    });
                    _messageController.clear();
                  }
                },
              ),
            ],
          ),
        ),
      ],
    ),
  );
}
} // 注意這個括號，用於結束 _ChatPageState 類的定義
class FullScreenVideoPage extends StatefulWidget {
  final VideoPlayerController controller;

  FullScreenVideoPage({required this.controller});

  @override
  _FullScreenVideoPageState createState() => _FullScreenVideoPageState();
}
class _FullScreenVideoPageState extends State<FullScreenVideoPage> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    super.initState();
    _controller = widget.controller;
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Video Player"),
        actions: [
          IconButton(
            icon: Icon(Icons.close),
            onPressed: () {
              Navigator.pop(context);
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: _controller.value.isInitialized
                  ? AspectRatio(
                      aspectRatio: _controller.value.aspectRatio,
                      child: VideoPlayer(_controller),
                    )
                  : CircularProgressIndicator(),
            ),
          ),
          VideoProgressIndicator(
            _controller,
            allowScrubbing: true,
          ),
          Text(
              "Total duration: ${_controller.value.duration.inSeconds} seconds"),
          ElevatedButton(
            onPressed: () {
              setState(() {
                _controller.value.isPlaying
                    ? _controller.pause()
                    : _controller.play();
              });
            },
            child: Icon(
              _controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
            ),
          ),
        ],
      ),
    );
  }
}
class MSNStyleChat extends StatefulWidget {

  List<String> favoriteList = ['Sam'];
  List<String> familyList = ['Mom', 'Dad'];
  List<String> colleagueList = ['Alice', 'Bob'];
  List<String> friendList = ['Charlie', 'Dave'];

  @override
  _MSNStyleChatState createState() => _MSNStyleChatState();
}
class _MSNStyleChatState extends State<MSNStyleChat> {
  bool showOtherButtons = true;
  bool showButtons = true; // 控制其他按钮的可见性
  bool showInputBox = true; // 控制输入框的可见性
  bool showSendButton = true; // 控制发送按钮的可见性
  bool showFavorites = false;
  bool showFamily = false;
  bool showColleagues = false;
  bool showFriends = false;
  bool showFriendsList = false; // Add this line
  bool showChatLog = false; // 新增這一行來跟踪是否應該顯示聊天記錄
  int currentSearchIndex = -1; // 當前搜索索引
  List<int> searchIndices = []; // 匹配的所有索引
  void navigateToChat(String friendName) {
  Navigator.push(
  context,
  MaterialPageRoute(
  builder: (context) => ChatPage(friendName: friendName), // 傳入 friendName
  ),
  );
  }
  void _findSearchIndices() {
    searchIndices.clear();
    String query = _searchController.text.toLowerCase();
    for (int i = 0; i < messages.length; i++) {
      if (messages[i]['content'].toString().toLowerCase().contains(query)) {
        searchIndices.add(i);
      }
    }
  }
  Widget highlightText(String text, String query) {
    List<String> splitText = text.split(query);
    List<Widget> widgets = [];
    for (var i = 0; i < splitText.length; i++) {
      widgets.add(Text(splitText[i]));
      if (i < splitText.length - 1) {
        widgets.add(
          Text(
            query,
            style: TextStyle(backgroundColor: Colors.yellow),
          ),
        );
      }
    }
    return RichText(
      text: TextSpan(
        style: TextStyle(color: Colors.black),
        children: widgets
            .map((w) =>
                TextSpan(text: (w as Text).data, style: (w as Text).style))
            .toList(),
      ),
    );
  }
  void _highlightNext() {
    if (searchIndices.isNotEmpty) {
      currentSearchIndex = (currentSearchIndex + 1) % searchIndices.length;
      _scrollToIndex(searchIndices[currentSearchIndex]);
    }
  }
  void _highlightPrevious() {
    if (searchIndices.isNotEmpty) {
      currentSearchIndex = (currentSearchIndex - 1 + searchIndices.length) %
          searchIndices.length;
      _scrollToIndex(searchIndices[currentSearchIndex]);
    }
  }
  void _scrollToIndex(int index) {
    _scrollController.animateTo(
      index * 80.0,
      duration: Duration(seconds: 1),
      curve: Curves.easeInOut,
    );
  }
  TextEditingController _searchController = TextEditingController();
  TextEditingController _messageController = TextEditingController();
  ScrollController _scrollController = ScrollController();
  List<Map<String, dynamic>> messages = [];
  TapDownDetails? tapPosition;
  int? selectedImageIndex;
  VideoPlayerController? _videoPlayerController;
  String searchQuery = "";

  void _searchAndScrollToMessage() {
    _findSearchIndices();
    _highlightNext();
    searchQuery = _searchController.text;
    int index = messages.indexWhere((message) => message['content']
        .toString()
        .toLowerCase()
        .contains(searchQuery.toLowerCase()));
    if (_searchController.text.isEmpty) {
      setState(() {
        searchIndices.clear();
        currentSearchIndex = -1;
      });
      return;
    }
    if (index != -1) {
      _scrollController.animateTo(
        index * 80.0,
        duration: Duration(seconds: 1),
        curve: Curves.easeInOut,
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('搜尋不到'),
      ));
    }
  } //存儲當前的搜尋查詢

  @override
  void initState() {
    super.initState();
    messages = widget.messages;  // 初始化消息列表
    _searchController.addListener(_searchAndScrollToMessage);
    // Your other initializations
  }

  bool isMessageMatch(Map<String, dynamic> message) {
    if (message['type'] == 'text') {
      return message['content']
          .toLowerCase()
          .contains(searchQuery.toLowerCase());
    }
    return false;
  }

  VideoPlayerController? _videoPlayerControllerLocal;

  void _playVideoFullScreen(VideoPlayerController controller) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => FullScreenVideoPage(controller: controller),
      ),
    );
  }

  Future<void> _saveMedia(Map<String, dynamic> message) async {
    if (message['type'] == 'image' ||
        message['type'] == 'video' ||
        message['type'] == 'file') {
      final directory = await getApplicationDocumentsDirectory();
      final path = directory.path;
      final ext = message['type'] == 'image'
          ? '.png'
          : (message['type'] == 'video' ? '.mp4' : '.file');
      final file = File('$path/media$ext');
      await file.writeAsBytes(message['bytes'] as Uint8List);
      final result = await ImageGallerySaver.saveFile(file.path);
      if (result['isSuccess']) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('儲存成功!'),
            duration: Duration(seconds: 2),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('儲存失敗，請重試'),
            duration: Duration(seconds: 2),
          ),
        );
      }
    }
  }

  Future<void> _triggerVibration() async {
    print("Triggering Vibration"); // Debug output
    bool? hasVibrator = await Vibration.hasVibrator();
    if (hasVibrator == true) {
      print("Device has vibrator, vibrating now."); // Debug output
      Vibration.vibrate();
      _addMessage("((())) 正在敲你!"); // 添加一條消息到聊天窗口
    } else {
      print("Device doesn't have a vibrator."); // Debug output
    }
  }

  @override
  void dispose() {
  for (var message in messages) {
  // 做一些清理工作，如果有的話
  }
  _searchController.dispose();
  if (_videoPlayerControllerLocal != null) {
  _videoPlayerControllerLocal!.dispose();
  }

  super.dispose();
  } //

  void _addMessage(String content, {String? type, Uint8List? bytes}) {
    final message = {
      'content': content,
      'type': type ?? 'text',
      'time': DateFormat('hh:mm a').format(DateTime.now()),
      'bytes': bytes,
    };

    if (type == 'video') {
      final tempDir = Directory.systemTemp;
      final file = File('${tempDir.path}/temp_video.mp4');
      file.writeAsBytesSync(bytes!);

      message['controller'] = VideoPlayerController.file(file)
        ..initialize().then((_) {
          setState(() {});
        });
    }
    setState(() {
      messages.add(message);
    });
  }

  Future<void> _pickImage() async {
    final pickedFile =
        await ImagePicker().pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      final bytes = await pickedFile.readAsBytes();
      _addMessage(pickedFile.path, type: 'image', bytes: bytes);
    }
  }

  Future<void> _pickVideo() async {
    final pickedFile =
        await ImagePicker().pickVideo(source: ImageSource.gallery);
    if (pickedFile != null) {
      final bytes = await pickedFile.readAsBytes();
      _videoPlayerController = VideoPlayerController.file(File(pickedFile.path))
        ..initialize().then((_) {
          setState(() {});
        });
      _addMessage(pickedFile.path, type: 'video', bytes: bytes);
    }
  }

  Future<void> _pickFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles();

      if (result != null) {
        File file = File(result.files.single.path!);
        print("File picked: ${file.path}");
      } else {
        print("User canceled file picking");
      }
    } catch (e) {
      print("Error picking file: $e");
    }
  }

  void _showMessageOptions(BuildContext context, int index) {
    final RenderBox overlay =
        Overlay.of(context).context.findRenderObject() as RenderBox;

    showMenu(
      context: context,
      position: RelativeRect.fromRect(
        tapPosition!.globalPosition & Size(40, 40),
        Offset.zero & overlay.size,
      ),
      items: <PopupMenuEntry<String>>[
        PopupMenuItem<String>(
          value: 'copy',
          child: Text('複製訊息'),
        ),
        PopupMenuItem<String>(
          value: 'delete',
          child: Text('刪除訊息'),
        ),
        PopupMenuItem<String>(
          value: 'recall',
          child: Text('回復訊息'),
        ),
      ],
    ).then((value) {
      if (value == 'copy') {
        Clipboard.setData(ClipboardData(text: messages[index]['content']));
      } else if (value == 'delete') {
        setState(() {
          messages.removeAt(index);
        });
      } else if (value == 'recall') {
        // Implement your recall action here
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("MSN "),
        actions: [
          IconButton(
            icon: Icon(Icons.home),
            onPressed: () {
              setState(() {
                showFriendsList = true;
                showChatLog = false;
                showButtons = false; // 设置为 false 以隐藏其他按钮
                showInputBox = false; // 设置为 false 以隐藏输入框
                showSendButton = false; // 设置为 false 以隐藏发送按钮
              });
            },
          ),
          IconButton(
            icon: Icon(Icons.chat),
            onPressed: () {
              setState(() {
                showChatLog = true;
                showFriendsList = false;
                showOtherButtons = false;  // Hide other buttons and TextField
                messages.add({
                  'sender': 'Sam',
                  'content': '晚安',
                  'time': 'PM 06:20',
                  'type': 'text',
                });
              });
            },
          ),

          IconButton(
            icon: Icon(Icons.settings),
            onPressed: () {},
          ),
        ],
      ),
      body: Column(
        children: [
          _searchController.text.isNotEmpty // 檢查搜索框是否為空
              ? Row(
                  children: [
                    ElevatedButton(
                      onPressed: _highlightPrevious,
                      child: Text("向上"),
                    ),
                    ElevatedButton(
                      onPressed: _highlightNext,
                      child: Text("向下"),
                    ),
                  ],
                )
              : Container(), // 如果搜索框是空的，則不顯示任何東西
          showChatLog  // 檢查是否顯示聊天紀錄
              ? Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              if (showOtherButtons)
                IconButton(
                  icon: Icon(Icons.image),
                  onPressed: _pickImage,
                ),
              if (showOtherButtons)
                IconButton(
                  icon: Icon(Icons.videocam),
                  onPressed: _pickVideo,
                ),
              if (showOtherButtons)
                IconButton(
                  icon: Icon(Icons.attach_file),
                  onPressed: _pickFile,
                ),
              if (showOtherButtons)
                IconButton(
                  icon: Icon(Icons.vibration),
                  onPressed: _triggerVibration,
                ),
              if (showOtherButtons)
                TextField(
                  controller: _searchController,
                  decoration: InputDecoration(
                    hintText: "Search...",
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
            ],
          )
              : Container(),  // 如果不是，則不顯示這些按鈕
          Expanded(
            child: showFriendsList
                ? ListView(
              children: [
                ListTile(
                  title: Text("最愛 (${widget.favoriteList.length})"),
                  onTap: () {
                    setState(() {
                      showFavorites = !showFavorites;
                    });
                  },
                ),
                if (showFavorites)
                  ...widget.favoriteList.map((friend) => ListTile(
                    title: Text(" $friend", style: TextStyle(color: Colors.blue)),
                    onTap: () {
                      navigateToChat(friend);  // 調用 navigateToChat 函數
                    },
                  )).toList(),
                      ListTile(
                        title: Text("家人 (${widget.familyList.length})"),
                        onTap: () {
                          setState(() {
                            showFamily = !showFamily;
                          });
                        },
                      ),
                      if (showFamily)
                        ...widget.familyList.map((family) => ListTile(title: Text(" $family", style: TextStyle(color: Colors.blue)))).toList(),

                      ListTile(
                        title: Text("同事 (${widget.colleagueList.length})"),
                        onTap: () {
                          setState(() {
                            showColleagues = !showColleagues;
                          });
                        },
                      ),
                      if (showColleagues)
                        ...widget.colleagueList.map((colleague) => ListTile(title: Text(" $colleague", style: TextStyle(color: Colors.blue)))).toList(),

                      ListTile(
                        title: Text("朋友 (${widget.friendList.length})"),
                        onTap: () {
                          setState(() {
                            showFriends = !showFriends;
                          });
                        },
                      ),
                      if (showFriends)
                        ...widget.friendList.map((friend) => ListTile(title: Text(" $friend", style: TextStyle(color: Colors.blue)))).toList(),
                    ],
                  )

                : showChatLog
                    ? ListView()
                    : messages.isEmpty // Check if messages are empty
                        ? Center(
                            child: Text(
                                "尚未有對話紀錄"), // Display this text when no messages
                          )
                        : ListView.builder(
                            controller: _scrollController,
                            itemCount: messages.length,
                            itemBuilder: (context, index) {
                              bool localShouldHighlight =
                                  searchIndices.contains(index);
                              final message = messages[index];
                              // bool isHighlighted = message['content']
                              toString()
                                  .toLowerCase()
                                  .contains(searchQuery.toLowerCase());
                              Widget contentWidget;

                              if (message['type'] == 'text') {
                                contentWidget = Column(
                                  crossAxisAlignment: CrossAxisAlignment.end,
                                  children: [
                                    localShouldHighlight // 使用新的局部變量
                                        ? highlightText(message['content'],
                                            _searchController.text)
                                        : Text(
                                            message['content'],
                                            style:
                                                TextStyle(color: Colors.blue),
                                          ),
                                    Text(
                                      message['time'],
                                      style: TextStyle(fontSize: 12),
                                    ),
                                  ],
                                );
                              } else if (message['type'] == 'image') {
                                contentWidget = Column(
                                  crossAxisAlignment: CrossAxisAlignment.end,
                                  children: [
                                    GestureDetector(
                                      onTap: () {
                                        showDialog(
                                          context: context,
                                          builder: (context) {
                                            return Dialog(
                                              child: Image.memory(
                                                message['bytes'] as Uint8List,
                                                fit: BoxFit.contain,
                                              ),
                                            );
                                          },
                                        );
                                      },
                                      child: Image.memory(
                                        message['bytes'] as Uint8List,
                                        fit: BoxFit.contain,
                                        width: 100, // 限制寬度
                                      ),
                                    ),
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.end,
                                      children: [
                                        IconButton(
                                          icon: Icon(Icons.save),
                                          onPressed: () async {
                                            await _saveMedia(message);
                                          },
                                        ),
                                        Text(
                                          message['time'],
                                          style: TextStyle(fontSize: 12),
                                        ),
                                      ],
                                    ),
                                  ],
                                );
                              } else if (message['type'] == 'video') {
                                VideoPlayerController? controller =
                                    message['controller'];
                                contentWidget = Column(
                                  crossAxisAlignment: CrossAxisAlignment.end,
                                  children: [
                                    controller != null &&
                                            controller.value.isInitialized
                                        ? Stack(
                                            children: [
                                              AspectRatio(
                                                aspectRatio: controller
                                                    .value.aspectRatio,
                                                child: VideoPlayer(controller),
                                              ),
                                              Positioned.fill(
                                                child: IconButton(
                                                  icon: Icon(
                                                    controller.value.isPlaying
                                                        ? Icons.pause
                                                        : Icons.play_arrow,
                                                    color: Colors.black,
                                                  ),
                                                  onPressed: () {
                                                    _playVideoFullScreen(
                                                        controller); // 在這裡調用新函數
                                                  },
                                                ),
                                              ),
                                            ],
                                          )
                                        : Text("Loading video..."),
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.end,
                                      children: [
                                        IconButton(
                                          icon: Icon(Icons.save),
                                          onPressed: () async {
                                            await _saveMedia(message);
                                          },
                                        ),
                                        Text(
                                          message['time'],
                                          style: TextStyle(fontSize: 12),
                                        ),
                                      ],
                                    ),
                                  ],
                                );
                              } else if (message['type'] == 'file') {
                                contentWidget = Text(
                                  "File: ${message['content']}",
                                );
                              } else {
                                contentWidget = Text("Unknown type");
                              }
                              // Check if this message index is in the search results
                              return GestureDetector(
                                onTapDown: (details) => tapPosition = details,
                                onLongPress: () {
                                  _showMessageOptions(context, index);
                                },
                                child: Align(
                                  alignment: Alignment.centerRight,
                                  child: Container(
                                    constraints: BoxConstraints(maxWidth: 200),
                                    padding: EdgeInsets.all(8.0),
                                    margin: EdgeInsets.all(8.0),
                                    decoration: BoxDecoration(
                                      color: (message['type'] == 'text' && localShouldHighlight)
                                          ? Colors.yellow // 如果是文本並需要高亮，則設為黃色
                                          : (message['type'] == 'text' ? Colors.grey[300] : null), // 如果是文本但不需要高亮，則設為灰色；否則為 null
                                      borderRadius: BorderRadius.circular(12),
                                    ),
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.end,
                                      children: [
                                        contentWidget,
                                      ],
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              if (showButtons)
                IconButton(
                  icon: Icon(Icons.image),
                  onPressed: _pickImage,
                ),
              if (showButtons)
                IconButton(
                  icon: Icon(Icons.videocam),
                  onPressed: _pickVideo,
                ),
              if (showButtons)
                IconButton(
                  icon: Icon(Icons.attach_file),
                  onPressed: _pickFile,
                ),
              if (showButtons)
                IconButton(
                  icon: Icon(Icons.vibration), // 震動圖標
                  onPressed: _triggerVibration, // 觸發震動的函數
              ),
            ],
          ),
          if (showInputBox)
            Container(
              padding: EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _messageController,
                      decoration: InputDecoration(
                        hintText: "請輸入...",
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                  if (showSendButton)
                    IconButton(
                      icon: Icon(Icons.send),
                      onPressed: () async {
                        String messageText = _messageController.text;
                        if (messageText.isNotEmpty) {
                          _addMessage(messageText); // 将用户的消息添加到聊天窗口
                          _messageController.clear(); // 清空输入框
                          try {
                            String translatedText = await fetchGPT3Response(
                                "Translate the following to English: $messageText"); // 获取翻译
                            _addMessage(translatedText); // 将翻译结果添加到聊天窗口
                          } catch (e) {
                            print("Error fetching GPT-3 Response: $e");
                      }
                    }
                  },
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
