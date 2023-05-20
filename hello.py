from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from dbConfig import conn,cur

# get user info
async def getUser(update,context):
    sql = "select * from all_user where `id`=%s;"
    cur.execute(sql,(str(update.message.from_user.id),))
    record = cur.fetchall()
    if len(record)==0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered")
    else:
        uid = record[0][0]
        uname = record[0][1]
        utype = record[0][2]
        if utype=="u":
            await update.message.reply_text("your id: "+uid+" name: "+uname+" type: user")
        else:
            await update.message.reply_text("your id: "+uid+" name: "+uname+" type: admin")

# create user
async def addUser(update,context):
    sql = "select * from all_user where `id`=%s;"
    cur.execute(sql,(str(update.message.from_user.id),))
    record = cur.fetchall()
    if len(record)==0:
        sql = "insert into all_user(id,name,type) values(%s,%s,%s);"
        cur.execute(sql,(str(update.message.from_user.id),str(update.message.from_user.full_name),'u'))
        conn.commit()
        await update.message.reply_text("create user "+str(update.message.from_user.id)+" successfully")
    else:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" has registered")

# show all command
async def allCommand(update,context):
    sql = "select * from all_user where `id`=%s;"
    cur.execute(sql,(str(update.message.from_user.id),))
    record = cur.fetchall()
    if len(record)==0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        if utype == "u":
            sql = "select * from all_command where `type`=%s;"
            cur.execute(sql,("u",))
            record = cur.fetchall()
            result = "all command:\n"
            for i in range(len(record)):
                result += record[i][1]+" "+record[i][2]+"\n"
            await update.message.reply_text(result)
        else:
            sql = "select * from all_command;"
            cur.execute(sql,())
            record = cur.fetchall()
            result = "all command:\n"
            for i in range(len(record)):
                result += record[i][1]+" "+record[i][2]+"\n"
            await update.message.reply_text(result)

def main():
    # bot token
    app = ApplicationBuilder().token("6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg").build()
    # all command
    all_command = [["ac",allCommand],["gu",getUser],["au",addUser]]
    for i in range(len(all_command)):
        app.add_handler(CommandHandler(all_command[i][0],all_command[i][1]))
    # run bot
    app.run_polling()

main()
