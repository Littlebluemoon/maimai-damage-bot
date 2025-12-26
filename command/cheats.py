from discord.ext import commands

from exceptions.RhythmException import InvalidBeatDivisionException, InvalidBPMException


@commands.command()
async def mash(ctx, bpm: float, division: int):
    try:
        if int(division) - division != 0 or division <= 0:
            raise InvalidBeatDivisionException("Beat divisor must be a nonzero integer.")
        if bpm <= 0 or bpm > 60000000:
            raise InvalidBPMException("BPM must be between 0 and 60000000 (not inclusive).")
        if bpm > 0 and division > 0:
            bpm = float(bpm)
            division = int(division)
            dist = 240.00 / bpm / division * 1000
            crit = 0 if dist - 33.3333 > 0 else 33.3333 - dist
            perf = 0 if dist - 100 > 0 else 100 - dist
            msg = f"""
            At **{bpm}** BPM, two 1/{division} notes are `{round(100 * dist) / 100} ms` apart.
    - The amount of time that the CRITICAL PERFECT judgment overlaps is `{round(100 * crit) / 100} ms` 
    - The amount of time that the PERFECT judgment overlaps is `{round(100 * perf) / 100} ms`
    Assuming that you are trying to hit a trill by hitting both of its buttons at the same time, then:"""
            if crit < 0:
                crit_decide = "- :information_source: This is one of the rare situations where you can mash the " \
                             "buttons at the same time and achieve CRITICAL PERFECT for both inputs, assuming" \
                             " that you have the strength to do so.\n"
                crit_decide += f"    - This requires at least **{round(50000 / dist) / 100}** hits per second with " \
                              f"both of your hands. "
            else:
                crit_decide = "- :information_source: You cannot mash both the buttons at the same time" \
                             " and get CRITICAL PERFECT for both notes. This is virtually impossible in maimai, anyway.\n"
            if perf == 0:
                perf_decide = "- :x: You cannot hit both the buttons at the same time and get PERFECT for both notes, " \
                             "because their PERFECT windows don't overlap at all.\n"
            elif perf <= 20.0000:
                perf_decide = "- :warning: You have a slight window to hit both the buttons and get PERFECT for" \
                             "both notes, but every of your inputs have to be (almost) frame perfect, " \
                             "or even worse. Consider trilling normally.\n"
            else:
                perf_decide = "- :white_check_mark: You have a reasonably comfortable window of time to hit both " \
                             "buttons at the same time and get PERFECT for both notes. Just be wary of your " \
                             "physical capabilities, whether you could hit at that speed consistently or not.\n"
            if perf > 0:
                perf_decide += f"    - If you attempt to do so, both of your hands must hit " \
                              f"at **{round(50000 / dist) / 100}** hit per second."
            msg += f"\n{crit_decide}{perf_decide}"
            await ctx.send(msg)
    except InvalidBeatDivisionException as e:
        await ctx.send(str(e))
    except InvalidBPMException as e:
        await ctx.send(str(e))

@commands.command()
async def hold(ctx, bpm, duration):
    bpm = float(bpm)
    duration_frac = duration.split(':')
    if bpm <= 0:
        await ctx.send("BPM must be a positive number.")
    else:
        if int(duration_frac[0]) <= 0:
            await ctx.send("Beat division denominator must be greater than zero.")
        if int(duration_frac[0]) > 1920:
            await ctx.send("Beat division denominator must be 1920 or less.")
        elif int(duration_frac[1]) < 0:
            await ctx.send("Beat division numerator cannot be negative.")
        else:
            hold_duration = 240 / bpm * int(duration_frac[1]) / int(duration_frac[0])
            if hold_duration >= 360:
                await ctx.send("I know, I know, but the game doesn't have a hold that long...")
            else:
                can_tap = (hold_duration <= 0.3)
                judge_str = f"The duration of the hold you inputted is {round(hold_duration, 2)}s.\n"
                if can_tap:
                    judge_str += "- :white_check_mark: You can simply clear the note with a single tap, guaranteeing at least Perfect or above."
                else:
                    judge_str += (f"- :warning: You have to actually hold the note to clear it.\n"
                                  f"- You need to hold it for at least **{(round(hold_duration - 0.2, 2))}s** for a Critical Perfect, or "
                                  f"**{(round((hold_duration - 0.2) * 0.66, 2))}s** for a Low Perfect.")
    await ctx.send(judge_str)