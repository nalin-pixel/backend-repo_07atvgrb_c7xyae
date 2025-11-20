import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Listing

app = FastAPI(title="Second-Hand Women's Clothing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Second-hand women's clothing backend is running"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# Helper to convert ObjectId to string in responses
class ListingOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    price: float
    category: str
    size: Optional[str] = None
    brand: Optional[str] = None
    condition: Optional[str] = None
    images: Optional[List[str]] = []
    location: Optional[str] = None


@app.post("/api/listings", response_model=dict)
def create_listing(listing: Listing):
    try:
        listing_id = create_document("listing", listing)
        return {"id": listing_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/listings", response_model=List[ListingOut])
def list_listings(category: Optional[str] = None, q: Optional[str] = None):
    try:
        filter_dict = {}
        if category:
            filter_dict["category"] = category
        if q:
            # simple text search across a few fields
            filter_dict["$or"] = [
                {"title": {"$regex": q, "$options": "i"}},
                {"description": {"$regex": q, "$options": "i"}},
                {"brand": {"$regex": q, "$options": "i"}},
            ]
        docs = get_documents("listing", filter_dict=filter_dict or None, limit=None)
        listings: List[ListingOut] = []
        for d in docs:
            listings.append(
                ListingOut(
                    id=str(d.get("_id")),
                    title=d.get("title"),
                    description=d.get("description"),
                    price=d.get("price"),
                    category=d.get("category"),
                    size=d.get("size"),
                    brand=d.get("brand"),
                    condition=d.get("condition"),
                    images=d.get("images", []),
                    location=d.get("location"),
                )
            )
        return listings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
