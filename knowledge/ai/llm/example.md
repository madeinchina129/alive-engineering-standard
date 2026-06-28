class AIService {
  Future<String> call(String model, String prompt) async {
    try {
      return await _client.post('/v1/chat', body: {...});
    } catch (e) {
      return _fallback(prompt); // 降级
    }
  }
}