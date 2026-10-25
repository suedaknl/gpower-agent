import os
import json
from openai import OpenAI
from mcp_server import t2_indep_sample_size, t2_indep_power

# Ortam değişkeninden API anahtarını çeker (Terminalde ayarlanmış olmalıdır)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "t2_indep_sample_size",
            "description": "G*Power a priori analizi: Bağımsız iki grup t-testi için gerekli örneklem büyüklüğünü hesaplar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "d": {"type": "number", "description": "Etki büyüklüğü (Cohen's d)"},
                    "alpha": {"type": "number", "description": "Hata payı (örn. 0.05)"},
                    "power": {"type": "number", "description": "İstenen güç (örn. 0.8)"},
                    "tails": {"type": "integer", "description": "Kuyruk sayısı (1 veya 2)"},
                    "ratio": {"type": "number", "description": "N2/N1 oranı"}
                },
                "required": ["d"]
            }
        }
    }
]

def ask_agent(prompt: str):
    print(f"Kullanıcı: {prompt}")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        tools=tools
    )
    
    message = response.choices[0].message
    
    if message.tool_calls:
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            print(f"[Ajan Çalıştırıyor]: t2_indep_sample_size(**{args})")
            
            # MCP arayüzündeki aracı çağır
            result = t2_indep_sample_size(**args)
            print(f"[Motor Yanıtı]: {json.dumps(result, indent=2)}")
    else:
        print(message.content)

if __name__ == "__main__":
    # Test komutu
    ask_agent("İlaç ve plasebo grubunu karşılaştıracağımız iki yönlü bir test yapacağız. Etki büyüklüğü 0.5, alfa 0.05 ve gücümüz 0.8. Gruplar eşit. Toplam kaç kişi lazım?")