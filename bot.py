"total_links": len(results),
        "stats": dict(stats),
        "results": results
    }
    
    timestamp = int(time.time())
    filename = f"report_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(summary, f, indent=2)
    
    success = sum(1 for r in results if r["success"])
    print(f"\n🎉 DONE! {success}/{len(results)} successful")
    print(f"💾 Saved: {filename}")
    show_stats(stats)

async def main():
    if not BOT_TOKENS:
        print("❌ NO TOKENS!")
        return
        
    async with MultiAccountReporter(BOT_TOKENS) as reporter:
        links = []
        print(f"\n🔗 TELEGRAM REPORTER (1 Bot)")
        print("Reasons: spam, violence, child_abuse, pornography, copyright, fake, other")
        print("Format: paste_link [reason]\n")
        
        try:
            while True:
                line = input("> ").strip()
                if not line or line.lower() == 'quit':
                    break
                if line.lower() == 'status':
                    show_stats(reporter.stats)
                    continue
                    
                parts = line.split(maxsplit=1)
                link = parts[0]
                chat_id = reporter.extract_chat_id(link)
                
                if chat_id:
                    reason = parts[1].strip() if len(parts) > 1 else "spam"
                    links.append({"link": link, "reason": reason})
                    print(f"✅ Added [{len(links)}] {chat_id} ({reason})")
                else:
                    print("❌ Invalid link. Examples:")
                    print("  https://t.me/channel")
                    print("  t.me/+ABC123")
                    print("  @group")
        except KeyboardInterrupt:
            pass
        
        if links:
            print(f"\n🚀 Starting {len(links)} reports...")
            results = await reporter.bulk_report_links(links)
            save_results(results, dict(reporter.stats))

if name == "main":
    asyncio.run(main())
