# Get AliceCore
import sys
sys.path.insert(0, '../AliceCore')

# Python packages
from fastapi import FastAPI, HTTPException
from typing import Optional, Dict

# Get AliceCore modules
from AliceCore.AliceMemory.long_memory import AliceLongMemory
from AliceCore.AliceMemory.short_memory import AliceShortMemory

app = FastAPI()

# Custom memory manager to handle short and long memories
class MemoryManager:
    short_memories: Dict[str, AliceShortMemory] = {}
    long_memories: Dict[str, AliceLongMemory] = {}

    @classmethod
    async def init_short_memory(cls, memory_id: str):
        if memory_id not in cls.short_memories:
            cls.short_memories[memory_id] = AliceShortMemory()
            await cls.short_memories[memory_id].init_memory(memory_id)

    @classmethod
    async def add_to_short_memory(cls, memory_id: str, memory: dict):
        if memory_id not in cls.short_memories:
            raise HTTPException(status_code=404, detail="Short memory not found")
        await cls.short_memories[memory_id].add_to_memory(memory, memory_id)

    @classmethod
    async def get_from_short_memory(cls, memory_id: str):
        if memory_id not in cls.short_memories:
            raise HTTPException(status_code=404, detail="Short memory not found")
        return await cls.short_memories[memory_id].get_memory(memory_id)

    @classmethod
    async def remove_from_short_memory(cls, memory_id: str):
        if memory_id not in cls.short_memories:
            raise HTTPException(status_code=404, detail="Short memory not found")
        await cls.short_memories[memory_id].remove_from_memory(memory_id)

    @classmethod
    async def init_long_memory(cls, memory_id: str):
        if memory_id not in cls.long_memories:
            cls.long_memories[memory_id] = AliceLongMemory()
            
    @classmethod
    async def init_long_memory_qdrant(cls, memory_id: str, qdrant_url: Optional[str] = "localhost", qdrant_port: Optional[int] = 6333):
        if memory_id not in cls.long_memories:
            raise HTTPException(status_code=404, detail="Long memory not found")
        await cls.long_memories[memory_id].init_qdrant(qdrant_url, qdrant_port)
            
    @classmethod
    async def init_long_memory_embedding(cls, memory_id: str, embedding_model: Optional[str] = "all-MiniLM-L6-v2", size: Optional[int] = 384):
        if memory_id not in cls.long_memories:
            raise HTTPException(status_code=404, detail="Long memory not found")
        await cls.long_memories[memory_id].init_embedding(embedding_model, size)
        
    @classmethod
    async def create_collection(cls, memory_id: str, collection_name: str):
        if memory_id not in cls.long_memories:
            raise HTTPException(status_code=404, detail="Long memory not found")
        await cls.long_memories[memory_id].create_collection(collection_name)
    
    @classmethod
    async def add_to_long_memory(cls, memory_id: str, collection_name: str, memory: dict):
        if memory_id not in cls.long_memories:
            raise HTTPException(status_code=404, detail="Long memory not found")
        await cls.long_memories[memory_id].insert_into_collection(collection_name, memory)

    @classmethod
    async def get_from_long_memory(cls, memory_id: str, collection_name: str):
        if memory_id not in cls.long_memories:
            raise HTTPException(status_code=404, detail="Long memory not found")
        return await cls.long_memories[memory_id].search_in_collection(collection_name, "")

    @classmethod
    async def delete_collection(cls, memory_id: str, collection_name: str):
        if memory_id not in cls.long_memories:
            raise HTTPException(status_code=404, detail="Long memory not found")
        return await cls.long_memories[memory_id].delete_collection(collection_name)

@app.post("/alice_core/memory/short/init")
async def init_short_memory(memory_id: str):
    await MemoryManager.init_short_memory(memory_id)
    return {"message": "Short memory initialized successfully."}

@app.post("/alice_core/memory/short/add")
async def add_to_short_memory(memory_id: str, memory: dict):
    await MemoryManager.add_to_short_memory(memory_id, memory)
    return {"message": "Memory added to short memory successfully."}

@app.post("/alice_core/memory/short/get")
async def get_from_short_memory(memory_id: str):
    return await MemoryManager.get_from_short_memory(memory_id)

@app.post("/alice_core/memory/short/remove")
async def remove_from_short_memory(memory_id: str):
    await MemoryManager.remove_from_short_memory(memory_id)
    return {"message": "Memory removed from short memory successfully."}

@app.post("/alice_core/memory/long/init")
async def init_long_memory(memory_id: str):
    await MemoryManager.init_long_memory(memory_id)
    return {"message": "Long memory initialized successfully."}

@app.post("/alice_core/memory/long/init_qdrant")
async def init_long_memory_qdrant(memory_id: str, qdrant_url: Optional[str] = "localhost", qdrant_port: Optional[int] = 6333):
    await MemoryManager.init_long_memory_qdrant(memory_id, qdrant_url, qdrant_port)
    return {"message": "Long memory initialized successfully."}

@app.post("/alice_core/memory/long/init_embedding")
async def init_long_memory_embedding(memory_id: str, embedding_model: Optional[str] = "all-MiniLM-L6-v2", size: Optional[int] = 384):
    await MemoryManager.init_long_memory_embedding(memory_id, embedding_model, size)
    return {"message": "Long memory initialized successfully."}

@app.post("/alice_core/memory/long/create_collection")
async def create_collection(memory_id: str, collection_name: str):
    await MemoryManager.create_collection(memory_id, collection_name)
    return {"message": "Collection created successfully."}

@app.post("/alice_core/memory/long/add")
async def add_to_long_memory(memory_id: str, collection_name: str, memory: dict):
    await MemoryManager.add_to_long_memory(memory_id, collection_name, memory)
    return {"message": "Memory added to long memory successfully."}

@app.post("/alice_core/memory/long/get")
async def get_from_long_memory(memory_id: str, collection_name: str):
    return await MemoryManager.get_from_long_memory(memory_id, collection_name)

@app.post("/alice_core/memory/long/remove")
async def remove_from_long_memory(memory_id: str, collection_name: str):
    await MemoryManager.delete_collection(memory_id, collection_name)
    return {"message": "Memory removed from long memory successfully."}
