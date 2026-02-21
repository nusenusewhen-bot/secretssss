// index.js
const { Client, GatewayIntentBits, PermissionsBitField, EmbedBuilder } = require('discord.js');
require('dotenv').config();

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildBans
    ]
});

const PREFIX = '!';
const OWNER_ID = process.env.OWNER_ID; // Put your Discord ID in .env

client.once('ready', () => {
    console.log(`✅ Logged in as ${client.user.tag}`);
    console.log(`📊 Serving ${client.guilds.cache.size} guilds`);
});

client.on('messageCreate', async (message) => {
    if (message.author.bot) return;
    if (!message.content.startsWith(PREFIX)) return;

    const args = message.content.slice(PREFIX.length).trim().split(/ +/);
    const command = args.shift().toLowerCase();

    // !unbanall command
    if (command === 'unbanall') {
        // Check if user is bot owner
        if (message.author.id !== OWNER_ID) {
            return message.reply('❌ Only the bot owner can use this command.');
        }

        // Check if user has Ban Members permission
        if (!message.member.permissions.has(PermissionsBitField.Flags.BanMembers)) {
            return message.reply('❌ You need `Ban Members` permission to use this.');
        }

        // Check bot permissions
        if (!message.guild.members.me.permissions.has(PermissionsBitField.Flags.BanMembers)) {
            return message.reply('❌ I need `Ban Members` permission to unban users.');
        }

        try {
            // Fetch all bans
            const bans = await message.guild.bans.fetch();
            const banCount = bans.size;

            if (banCount === 0) {
                return message.reply('✅ No banned users found in this server.');
            }

            const confirmEmbed = new EmbedBuilder()
                .setTitle('⚠️ Confirm Mass Unban')
                .setDescription(`You are about to unban **${banCount}** user(s).\n\nThis may take a while due to Discord rate limits (approximately ${Math.ceil(banCount * 1.5)} seconds).`)
                .setColor(0xFFA500)
                .setFooter({ text: 'Type "confirm" to proceed or "cancel" to abort.' });

            const confirmMsg = await message.reply({ embeds: [confirmEmbed] });

            // Wait for confirmation
            const filter = m => m.author.id === message.author.id && ['confirm', 'cancel'].includes(m.content.toLowerCase());
            
            try {
                const collected = await message.channel.awaitMessages({ 
                    filter, 
                    max: 1, 
                    time: 30000, 
                    errors: ['time'] 
                });
                
                const response = collected.first().content.toLowerCase();
                
                if (response === 'cancel') {
                    return message.reply('❌ Operation cancelled.');
                }
            } catch (e) {
                return message.reply('⏰ Confirmation timed out. Operation cancelled.');
            }

            // Start unbanning
            const progressEmbed = new EmbedBuilder()
                .setTitle('🔄 Unbanning Users...')
                .setDescription(`Progress: 0/${banCount} (0%)`)
                .setColor(0x3498DB);

            const progressMsg = await message.channel.send({ embeds: [progressEmbed] });

            let unbanned = 0;
            let failed = 0;
            const failedUsers = [];
            const startTime = Date.now();

            // Convert collection to array
            const banArray = Array.from(bans.values());

            for (let i = 0; i < banArray.length; i++) {
                const ban = banArray[i];
                
                try {
                    await message.guild.members.unban(ban.user.id, `Mass unban by ${message.author.tag}`);
                    unbanned++;
                    
                    // Update progress every 5 users or on last user
                    if (i % 5 === 0 || i === banArray.length - 1) {
                        const percent = Math.round((unbanned / banCount) * 100);
                        const elapsed = Math.floor((Date.now() - startTime) / 1000);
                        
                        progressEmbed.setDescription(
                            `Progress: **${unbanned}/${banCount}** (${percent}%)\n` +
                            `✅ Successful: ${unbanned}\n` +
                            `❌ Failed: ${failed}\n` +
                            `⏱️ Elapsed: ${elapsed}s\n` +
                            `👤 Last: ${ban.user.tag}`
                        );
                        
                        await progressMsg.edit({ embeds: [progressEmbed] });
                    }

                    // Rate limit protection - wait 1 second between unbans
                    // Discord allows ~5 actions per second, but we play it safe
                    if (i < banArray.length - 1) {
                        await new Promise(resolve => setTimeout(resolve, 1000));
                    }

                } catch (error) {
                    failed++;
                    failedUsers.push(`${ban.user.tag} (${ban.user.id}) - ${error.message}`);
                    console.error(`Failed to unban ${ban.user.tag}:`, error);
                }
            }

            // Final report
            const endTime = Date.now();
            const duration = Math.floor((endTime - startTime) / 1000);

            const resultEmbed = new EmbedBuilder()
                .setTitle('✅ Mass Unban Complete')
                .setDescription(
                    `**Total Bans:** ${banCount}\n` +
                    `**Successfully Unbanned:** ${unbanned}\n` +
                    `**Failed:** ${failed}\n` +
                    `**Duration:** ${duration} seconds`
                )
                .setColor(failed > 0 ? 0xFFA500 : 0x00FF00)
                .setTimestamp();

            if (failedUsers.length > 0 && failedUsers.length <= 10) {
                resultEmbed.addFields({
                    name: 'Failed Users',
                    value: failedUsers.join('\n') || 'None'
                });
            } else if (failedUsers.length > 10) {
                resultEmbed.addFields({
                    name: 'Failed Users',
                    value: `${failedUsers.slice(0, 10).join('\n')}\n... and ${failedUsers.length - 10} more`
                });
            }

            await message.channel.send({ embeds: [resultEmbed] });

        } catch (error) {
            console.error('Unbanall error:', error);
            message.reply(`❌ An error occurred: ${error.message}`);
        }
    }

    // !help command
    if (command === 'help') {
        const helpEmbed = new EmbedBuilder()
            .setTitle('📋 Bot Commands')
            .setDescription('Available commands:')
            .addFields(
                { name: '!unbanall', value: 'Unban all banned users in the server (Owner only)' },
                { name: '!help', value: 'Show this help message' }
            )
            .setColor(0x3498DB)
            .setFooter({ text: `Requested by ${message.author.tag}` });

        message.reply({ embeds: [helpEmbed] });
    }
});

// Error handling
client.on('error', console.error);
process.on('unhandledRejection', console.error);

client.login(process.env.DISCORD_TOKEN);
