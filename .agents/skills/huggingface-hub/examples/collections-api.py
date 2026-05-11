"""
Collections API Example

Collections group models, datasets, Spaces, and papers on the Hub.
This example shows how to create, manage, and share collections.

Prerequisites:
    pip install huggingface_hub
    huggingface-cli login
"""

from huggingface_hub import (
    HfApi,
    get_collection,
    create_collection,
    add_collection_item,
    update_collection_item,
    delete_collection_item,
    delete_collection,
)

api = HfApi()


# =============================================================================
# VIEWING COLLECTIONS
# =============================================================================

def view_collection(collection_slug: str):
    """View details of a collection."""

    collection = get_collection(collection_slug)

    print(f"\n=== {collection.title} ===")
    print(f"Slug: {collection.slug}")
    print(f"Owner: {collection.owner}")
    print(f"Description: {collection.description}")
    print(f"Private: {collection.private}")
    print(f"\nItems ({len(collection.items)}):")

    for item in collection.items:
        print(f"  - [{item.item_type}] {item.item_id}")
        if item.note:
            print(f"    Note: {item.note}")


# Example: View a public collection
# view_collection("osanseviero/diffusion-models-course-65c0823ac0e47e4bfb7d6b10")


# =============================================================================
# CREATING COLLECTIONS
# =============================================================================

def create_my_collection(title: str, description: str, private: bool = False):
    """Create a new collection."""

    collection = create_collection(
        title=title,
        description=description,
        private=private
    )

    print(f"\nCreated collection: {collection.slug}")
    print(f"URL: https://huggingface.co/collections/{collection.slug}")

    return collection


# Example:
# collection = create_my_collection(
#     title="My Favorite LLMs",
#     description="A curated list of the best open-source language models",
#     private=False
# )


# =============================================================================
# ADDING ITEMS
# =============================================================================

def add_items_to_collection(collection_slug: str):
    """Add various items to a collection."""

    # Add a model
    add_collection_item(
        collection_slug=collection_slug,
        item_id="meta-llama/Llama-3.1-8B-Instruct",
        item_type="model",
        note="Great instruction-following model"
    )
    print("Added model")

    # Add a dataset
    add_collection_item(
        collection_slug=collection_slug,
        item_id="stanfordnlp/imdb",
        item_type="dataset",
        note="Classic sentiment analysis dataset"
    )
    print("Added dataset")

    # Add a Space
    add_collection_item(
        collection_slug=collection_slug,
        item_id="gradio/text-generation",
        item_type="space",
        note="Interactive text generation demo"
    )
    print("Added Space")

    # Add a paper
    add_collection_item(
        collection_slug=collection_slug,
        item_id="2307.09288",  # arXiv ID
        item_type="paper",
        note="Llama 2 paper"
    )
    print("Added paper")


# Example:
# add_items_to_collection("username/my-collection-xxx")


# =============================================================================
# UPDATING ITEMS
# =============================================================================

def update_item_note(collection_slug: str, item_id: str, new_note: str):
    """Update the note on a collection item."""

    update_collection_item(
        collection_slug=collection_slug,
        item_id=item_id,
        note=new_note
    )
    print(f"Updated note for {item_id}")


# Example:
# update_item_note(
#     "username/my-collection-xxx",
#     "meta-llama/Llama-3.1-8B-Instruct",
#     "Updated: Now with improved context length!"
# )


# =============================================================================
# REMOVING ITEMS
# =============================================================================

def remove_item(collection_slug: str, item_id: str):
    """Remove an item from a collection."""

    delete_collection_item(
        collection_slug=collection_slug,
        item_id=item_id
    )
    print(f"Removed {item_id} from collection")


# Example:
# remove_item("username/my-collection-xxx", "stanfordnlp/imdb")


# =============================================================================
# DELETING COLLECTIONS
# =============================================================================

def delete_my_collection(collection_slug: str):
    """Delete an entire collection."""

    # Be careful - this is permanent!
    delete_collection(collection_slug)
    print(f"Deleted collection: {collection_slug}")


# Example:
# delete_my_collection("username/my-collection-xxx")


# =============================================================================
# LISTING USER/ORG COLLECTIONS
# =============================================================================

def list_user_collections(username: str):
    """List all collections for a user or organization."""

    # Collections appear on user/org profile pages
    # Access via the web UI or API

    # Get user info with collections
    # Note: This requires web scraping or checking the profile page
    print(f"View collections at: https://huggingface.co/{username}")


# =============================================================================
# BUILDING A CURATED COLLECTION
# =============================================================================

def build_llm_collection():
    """Build a curated collection of LLMs."""

    # Create collection
    collection = create_collection(
        title="Best Open LLMs 2024",
        description="Curated list of top open-source language models for 2024",
        private=False
    )

    # Define items to add
    items = [
        {
            "id": "meta-llama/Llama-3.1-70B-Instruct",
            "type": "model",
            "note": "Meta's flagship open model - excellent reasoning"
        },
        {
            "id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "type": "model",
            "note": "MoE architecture - fast and efficient"
        },
        {
            "id": "Qwen/Qwen2.5-72B-Instruct",
            "type": "model",
            "note": "Strong multilingual capabilities"
        },
        {
            "id": "google/gemma-2-27b-it",
            "type": "model",
            "note": "Google's open model - good for research"
        },
        {
            "id": "deepseek-ai/DeepSeek-V3",
            "type": "model",
            "note": "Strong coding and math abilities"
        }
    ]

    # Add items
    for item in items:
        try:
            add_collection_item(
                collection_slug=collection.slug,
                item_id=item["id"],
                item_type=item["type"],
                note=item["note"]
            )
            print(f"Added: {item['id']}")
        except Exception as e:
            print(f"Failed to add {item['id']}: {e}")

    print(f"\nCollection created: https://huggingface.co/collections/{collection.slug}")
    return collection


# Example:
# collection = build_llm_collection()


# =============================================================================
# ORGANIZATION COLLECTIONS
# =============================================================================

def create_org_collection(org_name: str):
    """Create a collection for an organization."""

    collection = create_collection(
        title="Organization Resources",
        description="Official models and datasets from our organization",
        namespace=org_name,  # Creates under org instead of user
        private=False
    )

    print(f"Created org collection: {collection.slug}")
    return collection


# Example:
# create_org_collection("my-organization")


# =============================================================================
# DEMO
# =============================================================================

if __name__ == "__main__":
    print("Collections API Examples")
    print("========================\n")

    # View an example public collection
    print("Example: Viewing a public collection")
    try:
        collection = get_collection("osanseviero/diffusion-models-course-65c0823ac0e47e4bfb7d6b10")
        print(f"Title: {collection.title}")
        print(f"Items: {len(collection.items)}")
        print(f"First few items:")
        for item in collection.items[:3]:
            print(f"  - {item.item_type}: {item.item_id}")
    except Exception as e:
        print(f"Could not fetch collection: {e}")

    print("\n--- Done! ---")
    print("\nTo create your own collections, uncomment the examples above.")
