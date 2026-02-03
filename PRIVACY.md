# Privacy Policy - FGG Bot

## Last Updated: February 2, 2026

## 1. Introduction

This Privacy Policy explains how FGG Bot ("the Bot", "we", "our") collects, uses, and protects information when you use our Discord bot service. By using the Bot, you consent to the data practices described in this policy.

## 2. Information We Collect

### 2.1 Server Configuration Data

When the Bot is added to a Discord server, we collect and store:

- Guild ID - Unique identifier of the Discord server
- Channel ID - The channel where game notifications are sent (configured via /setup command)
- Role ID - The role mentioned in notifications (optional, configured via /setup command)

### 2.2 Game Listing Data

The Bot aggregates publicly available information about free game giveaways, including:

- Game titles, descriptions, and images
- Availability dates and pricing information
- Platform information (Epic Games Store, Steam)

This data is sourced from public APIs (Epic Games API, IGDB API) and web scraping, and does not contain any user-specific information.

### 2.3 Bot Activity Logs

For operational purposes, we log:

- Bot join/removal events from servers
- Configuration changes (channel and role updates via commands)
- Bot startup and operational status

We do not log:

- Individual user commands
- Message content
- User IDs or usernames
- Any personally identifiable information (PII)

### 2.4 Discord-Provided Analytics

We have access to standard Discord bot analytics, which includes:

- Total number of servers the Bot is present in
- Total member count across all servers

This information is provided automatically by Discord and cannot be disabled.

## 3. How We Use Your Information

We use collected data solely for the following purposes:

- Service Delivery: To send game giveaway notifications to configured channels
- Bot Configuration: To maintain server-specific notification settings
- Historical Tracking: To maintain a record of free game giveaways for future features (e.g., savings calculations)
- Technical Operations: To monitor Bot health, debug issues, and ensure reliable operation
- Service Improvement: To understand usage patterns and improve Bot functionality

We do not:

- Sell, rent, or share your data with third parties for marketing purposes
- Use your data for advertising or profiling
- Share data with third parties except as required for Bot operation (Discord API, game data sources)

## 4. Data Storage and Security

### 4.1 Storage

All configuration data is stored in a local MongoDB database secured on our hosting infrastructure. Game listing data is stored permanently for historical tracking and future features.

### 4.2 Data Retention

- Server Configuration Data: Retained while the Bot remains on your server
- After Bot Removal: All server-specific data (Guild ID, Channel ID, Role ID) is automatically deleted when the Bot is removed from your server
- Partial Removal: Using the /setup remove command deletes Channel ID and Role ID, but Guild ID remains until the Bot is fully removed from the server
- Game Listing Data: Stored permanently in our database to maintain a historical record of free game giveaways and enable future features

### 4.3 Security

We implement reasonable security measures to protect stored data, including:

- Restricted database access
- Encrypted connections to Discord API
- Regular security updates and monitoring

However, no method of electronic storage is 100% secure, and we cannot guarantee absolute security.

## 5. Third-Party Services

The Bot interacts with the following third-party services to provide functionality:

- Discord API - For bot communication and server interaction
- Epic Games API - To retrieve free game information from Epic Games Store
- Steam - Web scraping of publicly available free game data
- IGDB API - For additional game metadata and information

Each third-party service operates under its own privacy policy. We recommend reviewing:

- [Discord Privacy Policy](https://discord.com/privacy)
- [Epic Games Privacy Policy](https://legal.epicgames.com/en-US/epicgames/privacy-policy)
- [Steam Privacy Policy](https://store.steampowered.com/privacy_agreement)

## 6. Data Sharing and Disclosure

We do not sell or share your data with third parties, except:

- With Your Consent: When you explicitly authorize data sharing
- Legal Requirements: If required by law, court order, or government regulation
- Service Providers: Discord API and game data sources necessary for Bot operation
- Security Purposes: To investigate fraud, abuse, or violations of our Terms of Service

## 7. Your Rights and Choices

### 7.1 Data Access

You can request information about what data we store for your server by contacting us through our support channels.

### 7.2 Data Deletion

You have the right to request deletion of your server's data:

- Automatic Deletion: Remove the Bot from your server, and all data is automatically deleted
- Partial Deletion: Use /setup remove to delete notification configuration while keeping the Bot on your server
- Manual Request: Contact us for manual data deletion if needed

### 7.3 Opt-Out

You can stop data collection at any time by removing the Bot from your Discord server.

## 8. Children's Privacy

The Bot does not knowingly collect information from users under the age of 13 (or the applicable age of digital consent in your jurisdiction). If we become aware that we have collected data from a child without proper consent, we will delete that information promptly.

## 9. International Data Transfers

The Bot operates from servers located in the United States. By using the Bot, you consent to the transfer and processing of your data in the United States, which may have different data protection laws than your jurisdiction.

## 10. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. Changes will be communicated through:

- Updated "Last Updated" date at the top of this policy
- Announcements in our support server (if material changes occur)

Continued use of the Bot after changes constitutes acceptance of the updated Privacy Policy.

## 11. Contact Us

If you have questions, concerns, or requests regarding this Privacy Policy or your data, please contact us:

Support Server: [FGG BOT HUB](https://discord.gg/ED9tCRkxXe)
GitHub: [GITHUB](https://github.com/SoLvkky/fgg-bot)

## 12. Compliance

This Privacy Policy is designed to comply with:

- Discord Developer Terms of Service and Developer Policy
- General Data Protection Regulation (GDPR) principles
- California Consumer Privacy Act (CCPA) where applicable
- Other applicable data protection laws

---

## By using FGG Bot, you acknowledge that you have read, understood, and agree to this Privacy Policy
