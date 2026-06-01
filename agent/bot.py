from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gitlab_client import GitLabClient
from config import TELEGRAM_BOT_TOKEN
import logging

gitlab = GitLabClient()
logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 DevSecOps Agent Online\n\n"
        "/run_pipeline\n"
        "/scan\n"
        "/deploy\n"
        "/status\n"
        "/stop_pipeline\n"
        "/logs <job_id>"
    )


async def run_pipeline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.trigger_pipeline("full")

        await update.message.reply_text(
            f"🚀 Pipeline started\n\n"
            f"ID: {pipeline.get('id')}\n"
            f"Status: {pipeline.get('status')}\n"
            f"URL: {pipeline.get('web_url')}"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{str(e)}")


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.trigger_pipeline("scan")

        await update.message.reply_text(
            f"🛡️ Scan started\nID: {pipeline.get('id')}"
        )
    except Exception as e:
        await update.message.reply_text(str(e))


async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.trigger_pipeline("deploy")

        await update.message.reply_text(
            f"📦 Deploy started\nID: {pipeline.get('id')}"
        )
    except Exception as e:
        await update.message.reply_text(str(e))


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.get_latest_pipeline()

        if not pipeline:
            await update.message.reply_text("No pipeline found.")
            return

        jobs = gitlab.get_pipeline_jobs(pipeline["id"])

        jobs_text = "\n".join(
            f"- {j['name']} | {j['status']} | {j['id']}"
            for j in jobs
        )

        await update.message.reply_text(
            f"📊 Pipeline {pipeline['id']}\n"
            f"Status: {pipeline['status']}\n\n"
            f"Jobs:\n{jobs_text}"
        )

    except Exception as e:
        await update.message.reply_text(str(e))


async def stop_pipeline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.get_latest_pipeline()

        if not pipeline:
            await update.message.reply_text("No pipeline found.")
            return

        result = gitlab.cancel_pipeline(pipeline["id"])

        await update.message.reply_text(
            f"🛑 Cancelled pipeline {result['id']}"
        )

    except Exception as e:
        await update.message.reply_text(str(e))


async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("Usage: /logs <job_id>")
            return

        logs_text = gitlab.get_job_logs(context.args[0])

        await update.message.reply_text(logs_text[-3500:])

    except Exception as e:
        await update.message.reply_text(str(e))
        
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pipeline = gitlab.get_latest_pipeline()

        jobs = gitlab.get_pipeline_jobs(pipeline["id"])

        report_job = next(
            (j for j in jobs if j["name"] == "generate_report"),
            None
        )

        if not report_job:
            await update.message.reply_text("Report not ready yet.")
            return

        logs = gitlab.get_job_logs(report_job["id"])

        await update.message.reply_text(
            "📊 SCAN REPORT\n\n" + logs[-3500:]
        )

    except Exception as e:
        await update.message.reply_text(str(e))



def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run_pipeline", run_pipeline))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("deploy", deploy))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("stop_pipeline", stop_pipeline))
    app.add_handler(CommandHandler("logs", logs))
    app.add_handler(CommandHandler("report", report))
    print("🤖 DevSecOps bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()