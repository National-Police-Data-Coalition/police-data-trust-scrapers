page_1 = b"""

<!doctype html>
<html lang="en-us">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Commands : 50-a.org</title>
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css"
          integrity="sha384-HmYpsz2Aa9Gh3JlkCoh8kUJ2mUKJKTnkyC2Lzt8aLzpPOpnDe8KpFE2xNiBpMDou" crossorigin="anonymous">
    <link rel="stylesheet" href="/style.css">



    <style>
      section.section form.search {
        margin-top: 2em;
        margin-bottom: 2em;
        max-width: 32em;
      }
      section.section,
      header,
      footer {
        max-width: 769px;
        margin: auto;
      }
      header, footer {
        padding: 0.5em;
      }
    </style>
  </head>

  <body>
    <header>

      <form action="/search" method="GET">
        <label for="q" class="label">Search by Officer Name or Badge Number</label>
        <div class="field has-addons">
          <div class="control is-expanded">
            <input class="input" type="text" id="q" name="q" value="" placeholder="enter name or badge #" required>
          </div>
          <div class="control">
            <button class="button is-info" type="submit">Search</button>
          </div>
        </div>
      </form>
    </header>
    <section class="section commands">
  <div class="container">
    <div class="summary">
      <h1 class="title">NYPD Precincts and Units</h1>
      <p>
        Need to
        <a href="https://www1.nyc.gov/site/nypd/bureaus/patrol/find-your-precinct.page">find your Precinct</a>?
        Look it up at nyc.gov.
      </p>
      <br />
    </div>
  </div>
  <div class="container commands">
    <a href="/command/1pct" class="command">1st Precinct</a><br />
    <a href="/command/1det" class="command">1st Precinct Detective Squad</a><br />
    <a href="/command/5pct" class="command">5th Precinct</a><br />
    <a href="/command/5det" class="command">5th Precinct Detective Squad</a><br />
    <a href="/command/6pct" class="command">6th Precinct</a><br />
    <a href="/command/6det" class="command">6th Precinct Detective Squad</a><br />
    <a href="/command/7pct" class="command">7th Precinct</a><br />
    <a href="/command/7det" class="command">7th Precinct Detective Squad</a><br />
    <a href="/command/9pct" class="command">9th Precinct</a><br />
    <a href="/command/9det" class="command">9th Precinct Detective Squad</a><br />
    <a href="/command/10pct" class="command">10th Precinct</a><br />
    <a href="/command/10det" class="command">10th Precinct Detective Squad</a><br />
    <a href="/command/13pct" class="command">13th Precinct</a><br />
    <a href="/command/13det" class="command">13th Precinct Detective Squad</a><br />
    <a href="/command/17pct" class="command">17th Precinct</a><br />
    <a href="/command/17det" class="command">17th Precinct Detective Squad</a><br />
    <a href="/command/19pct" class="command">19th Precinct</a><br />
    <a href="/command/19det" class="command">19th Precinct Detective Squad</a><br />
    <a href="/command/20pct" class="command">20th Precinct</a><br />
    <a href="/command/20det" class="command">20th Precinct Detective Squad</a><br />
    <a href="/command/23pct" class="command">23rd Precinct</a><br />
    <a href="/command/23det" class="command">23rd Precinct Detective Squad</a><br />
    <a href="/command/24pct" class="command">24th Precinct</a><br />
    <a href="/command/24det" class="command">24th Precinct Detective Squad</a><br />
    <a href="/command/25pct" class="command">25th Precinct</a><br />
    <a href="/command/25det" class="command">25th Precinct Detective Squad</a><br />
    <a href="/command/26pct" class="command">26th Precinct</a><br />
    <a href="/command/26det" class="command">26th Precinct Detective Squad</a><br />
    <a href="/command/28pct" class="command">28th Precinct</a><br />
    <a href="/command/28det" class="command">28th Precinct Detective Squad</a><br />
    <a href="/command/30pct" class="command">30th Precinct</a><br />
    <a href="/command/30det" class="command">30th Precinct Detective Squad</a><br />
    <a href="/command/32pct" class="command">32nd Precinct</a><br />
    <a href="/command/32det" class="command">32nd Precinct Detective Squad</a><br />
    <a href="/command/33pct" class="command">33rd Precinct</a><br />
    <a href="/command/33det" class="command">33rd Precinct Detective Squad</a><br />
    <a href="/command/34pct" class="command">34th Precinct</a><br />
    <a href="/command/34det" class="command">34th Precinct Detective Squad</a><br />
    <a href="/command/40pct" class="command">40th Precinct</a><br />
    <a href="/command/40det" class="command">40th Precinct Detective Squad</a><br />
    <a href="/command/41pct" class="command">41st Precinct</a><br />
    <a href="/command/41det" class="command">41st Precinct Detective Squad</a><br />
    <a href="/command/42pct" class="command">42nd Precinct</a><br />
    <a href="/command/42det" class="command">42nd Precinct Detective Squad</a><br />
    <a href="/command/43pct" class="command">43rd Precinct</a><br />
    <a href="/command/43det" class="command">43rd Precinct Detective Squad</a><br />
    <a href="/command/44pct" class="command">44th Precinct</a><br />
    <a href="/command/44det" class="command">44th Precinct Detective Squad</a><br />
    <a href="/command/45pct" class="command">45th Precinct</a><br />
    <a href="/command/45det" class="command">45th Precinct Detective Squad</a><br />
    <a href="/command/46pct" class="command">46th Precinct</a><br />
    <a href="/command/46det" class="command">46th Precinct Detective Squad</a><br />
    <a href="/command/47pct" class="command">47th Precinct</a><br />
    <a href="/command/47det" class="command">47th Precinct Detective Squad</a><br />
    <a href="/command/48pct" class="command">48th Precinct</a><br />
    <a href="/command/48det" class="command">48th Precinct Detective Squad</a><br />
    <a href="/command/49pct" class="command">49th Precinct</a><br />
    <a href="/command/49det" class="command">49th Precinct Detective Squad</a><br />
    <a href="/command/50pct" class="command">50th Precinct</a><br />
    <a href="/command/50det" class="command">50th Precinct Detective Squad</a><br />
    <a href="/command/52pct" class="command">52nd Precinct</a><br />
    <a href="/command/52det" class="command">52nd Precinct Detective Squad</a><br />
    <a href="/command/60pct" class="command">60th Precinct</a><br />
    <a href="/command/60det" class="command">60th Precinct Detective Squad</a><br />
    <a href="/command/61pct" class="command">61st Precinct</a><br />
    <a href="/command/61det" class="command">61st Precinct Detective Squad</a><br />
    <a href="/command/62pct" class="command">62nd Precinct</a><br />
    <a href="/command/62det" class="command">62nd Precinct Detective Squad</a><br />
    <a href="/command/63pct" class="command">63rd Precinct</a><br />
    <a href="/command/63det" class="command">63rd Precinct Detective Squad</a><br />
    <a href="/command/66pct" class="command">66th Precinct</a><br />
    <a href="/command/66det" class="command">66th Precinct Detective Squad</a><br />
    <a href="/command/67pct" class="command">67th Precinct</a><br />
    <a href="/command/67det" class="command">67th Precinct Detective Squad</a><br />
    <a href="/command/68pct" class="command">68th Precinct</a><br />
    <a href="/command/68det" class="command">68th Precinct Detective Squad</a><br />
    <a href="/command/69pct" class="command">69th Precinct</a><br />
    <a href="/command/69det" class="command">69th Precinct Detective Squad</a><br />
    <a href="/command/70pct" class="command">70th Precinct</a><br />
    <a href="/command/70det" class="command">70th Precinct Detective Squad</a><br />
    <a href="/command/71pct" class="command">71st Precinct</a><br />
    <a href="/command/71det" class="command">71st Precinct Detective Squad</a><br />
    <a href="/command/72pct" class="command">72nd Precinct</a><br />
    <a href="/command/72det" class="command">72nd Precinct Detective Squad</a><br />
    <a href="/command/73pct" class="command">73rd Precinct</a><br />
    <a href="/command/73det" class="command">73rd Precinct Detective Squad</a><br />
    <a href="/command/75pct" class="command">75th Precinct</a><br />
    <a href="/command/75det" class="command">75th Precinct Detective Squad</a><br />
    <a href="/command/76pct" class="command">76th Precinct</a><br />
    <a href="/command/76det" class="command">76th Precinct Detective Squad</a><br />
    <a href="/command/77pct" class="command">77th Precinct</a><br />
    <a href="/command/77det" class="command">77th Precinct Detective Squad</a><br />
    <a href="/command/78pct" class="command">78th Precinct</a><br />
    <a href="/command/78det" class="command">78th Precinct Detective Squad</a><br />
    <a href="/command/79pct" class="command">79th Precinct</a><br />
    <a href="/command/79det" class="command">79th Precinct Detective Squad</a><br />
    <a href="/command/81pct" class="command">81st Precinct</a><br />
    <a href="/command/81det" class="command">81st Precinct Detective Squad</a><br />
    <a href="/command/83pct" class="command">83rd Precinct</a><br />
    <a href="/command/83det" class="command">83rd Precinct Detective Squad</a><br />
    <a href="/command/84pct" class="command">84th Precinct</a><br />
    <a href="/command/84det" class="command">84th Precinct Detective Squad</a><br />
    <a href="/command/88pct" class="command">88th Precinct</a><br />
    <a href="/command/88det" class="command">88th Precinct Detective Squad</a><br />
    <a href="/command/90pct" class="command">90th Precinct</a><br />
    <a href="/command/90det" class="command">90th Precinct Detective Squad</a><br />
    <a href="/command/94pct" class="command">94th Precinct</a><br />
    <a href="/command/94det" class="command">94th Precinct Detective Squad</a><br />
    <a href="/command/100pct" class="command">100th Precinct</a><br />
    <a href="/command/100det" class="command">100th Precinct Detective Squad</a><br />
    <a href="/command/101pct" class="command">101st Precinct</a><br />
    <a href="/command/101det" class="command">101st Precinct Detective Squad</a><br />
    <a href="/command/102pct" class="command">102nd Precinct</a><br />
    <a href="/command/102det" class="command">102nd Precinct Detective Squad</a><br />
    <a href="/command/103pct" class="command">103rd Precinct</a><br />
    <a href="/command/103det" class="command">103rd Precinct Detective Squad</a><br />
    <a href="/command/104pct" class="command">104th Precinct</a><br />
    <a href="/command/104det" class="command">104th Precinct Detective Squad</a><br />
    <a href="/command/105pct" class="command">105th Precinct</a><br />
    <a href="/command/105det" class="command">105th Precinct Detective Squad</a><br />
    <a href="/command/106pct" class="command">106th Precinct</a><br />
    <a href="/command/106det" class="command">106th Precinct Detective Squad</a><br />
    <a href="/command/107pct" class="command">107th Precinct</a><br />
    <a href="/command/107det" class="command">107th Precinct Detective Squad</a><br />
    <a href="/command/108pct" class="command">108th Precinct</a><br />
    <a href="/command/108det" class="command">108th Precinct Detective Squad</a><br />
    <a href="/command/109pct" class="command">109th Precinct</a><br />
    <a href="/command/109det" class="command">109th Precinct Detective Squad</a><br />
    <a href="/command/110pct" class="command">110th Precinct</a><br />
    <a href="/command/110det" class="command">110th Precinct Detective Squad</a><br />
    <a href="/command/111pct" class="command">111th Precinct</a><br />
    <a href="/command/111det" class="command">111th Precinct Detective Squad</a><br />
    <a href="/command/112pct" class="command">112th Precinct</a><br />
    <a href="/command/112det" class="command">112th Precinct Detective Squad</a><br />
    <a href="/command/113pct" class="command">113th Precinct</a><br />
    <a href="/command/113det" class="command">113th Precinct Detective Squad</a><br />
    <a href="/command/114pct" class="command">114th Precinct</a><br />
    <a href="/command/114det" class="command">114th Precinct Detective Squad</a><br />
    <a href="/command/115pct" class="command">115th Precinct</a><br />
    <a href="/command/115det" class="command">115th Precinct Detective Squad</a><br />
    <a href="/command/120pct" class="command">120th Precinct</a><br />
    <a href="/command/120det" class="command">120th Precinct Detective Squad</a><br />
    <a href="/command/121pct" class="command">121st Precinct</a><br />
    <a href="/command/121det" class="command">121st Precinct Detective Squad</a><br />
    <a href="/command/122pct" class="command">122nd Precinct</a><br />
    <a href="/command/122det" class="command">122nd Precinct Detective Squad</a><br />
    <a href="/command/123pct" class="command">123rd Precinct</a><br />
    <a href="/command/123det" class="command">123rd Precinct Detective Squad</a><br />
    <a href="/command/442" class="command">Administration Division</a><br />
    <a href="/command/538" class="command">Arson and Explosion Squad</a><br />
    <a href="/command/163" class="command">Auto Crime</a><br />
    <a href="/command/586" class="command">Auxiliary Police Section</a><br />
    <a href="/command/306" class="command">Aviation Unit</a><br />
    <a href="/command/707" class="command">BH Division</a><br />
    <a href="/command/391" class="command">Barrier Section</a><br />
    <a href="/command/21" class="command">Bomb Squad</a><br />
    <a href="/command/89" class="command">Bronx Court Section</a><br />
    <a href="/command/189" class="command">Bronx Robbery Squad</a><br />
    <a href="/command/478" class="command">Bronx Special Victims Squad</a><br />
    <a href="/command/589" class="command">Bronx Special Victims Squad</a><br />
    <a href="/command/754" class="command">Bronx Standards and Assessment Unit</a><br />
    <a href="/command/36" class="command">Brooklyn Court Section</a><br />
    <a href="/command/252" class="command">Brooklyn Robbery Squad</a><br />
    <a href="/command/313" class="command">Brooklyn Special Victims Squad</a><br />
    <a href="/command/755" class="command">Brooklyn Standards and Assessment Unit</a><br />
    <a href="/command/302" class="command">Building Maintenance Section</a><br />
    <a href="/command/732" class="command">Business Improvement Deployment Team</a><br />
    <a href="/command/730" class="command">CCRB Liaison Unit</a><br />
    <a href="/command/744" class="command">CIO</a><br />
    <a href="/command/736" class="command">Campus Management Section</a><br />
    <a href="/command/267" class="command">Central Investigation and Research Division</a><br />
    <a href="/command/CPKdet" class="command">Central Park Detective Squad</a><br />
    <a href="/command/CPKpct" class="command">Central Park Precinct</a><br />
    <a href="/command/519" class="command">Chaplains Unit</a><br />
    <a href="/command/342" class="command">Chief of Department Investigation Review Section</a><br />
    <a href="/command/145" class="command">Chief of Department Office</a><br />
    <a href="/command/784" class="command">Chief of Department Rapid Response Unit</a><br />
    <a href="/command/393" class="command">Chief of Special Operations</a><br />
    <a href="/command/537" class="command">City Wide Counterterrorism Unit</a><br />
    <a href="/command/435" class="command">Cold Case Squad</a><br />
    <a href="/command/91" class="command">Communications Division</a><br />
    <a href="/command/CAB" class="command">Community Affairs Bureau</a><br />
    <a href="/command/40" class="command">Community Affairs Bureau Community Outreach Division</a><br />
    <a href="/command/789" class="command">Comp Division Body Worn Camera Unit</a><br />
    <a href="/command/608" class="command">Contract Administration Unit</a><br />
    <a href="/command/316" class="command">Counterterrorism Division</a><br />
    <a href="/command/266" class="command">Counterterrorism Lower Manhattan Security Initiative</a><br />
    <a href="/command/739" class="command">Court Monitoring Section</a><br />
    <a href="/command/232" class="command">Crime Control Strategies</a><br />
    <a href="/command/564" class="command">Crime Prevention Division</a><br />
    <a href="/command/229" class="command">Crime Scene Unit</a><br />
    <a href="/command/10" class="command">Criminal Intelligence Section</a><br />
    <a href="/command/341" class="command">Criminal Justice Bureau</a><br />
    <a href="/command/CRC" class="command">Critical Response Command</a><br />
    <a href="/command/247" class="command">DA Bronx</a><br />
    <a href="/command/353" class="command">DA Brooklyn</a><br />
    <a href="/command/404" class="command">DA New York</a><br />
    <a href="/command/113" class="command">DA Queens</a><br />
    <a href="/command/407" class="command">DA Staten Island</a><br />
    <a href="/command/812" class="command">DB Brooklyn North Video Collection Team</a><br />
    <a href="/command/807" class="command">DB Brooklyn South Video Collection Team</a><br />
    <a href="/command/813" class="command">DB Queens Video Collection Team</a><br />
    <a href="/command/814" class="command">DB Queens Video Collection Team</a><br />
    <a href="/command/788" class="command">Data Analysis and Mapping Section</a><br />
    <a href="/command/741" class="command">Dep Comm Community Partnerships</a><br />
    <a href="/command/742" class="command">Dep Comm Community Partnerships YSU</a><br />
    <a href="/command/573" class="command">Department Comm Employee Relations</a><br />
    <a href="/command/502" class="command">Department Comm Employee Relations CU</a><br />
    <a href="/command/544" class="command">Department Comm Equity &amp; Inclusion</a><br />
    <a href="/command/667" class="command">Department Comm Intel &amp; Counterterrorism</a><br />
    <a href="/command/462" class="command">Department of Investigation Squad</a><br />
    <a href="/command/455" class="command">Deputy Commissioner Department Advocate Office</a><br />
    <a href="/command/627" class="command">Deputy Commissioner Labor Relations</a><br />
    <a href="/command/591" class="command">Deputy Commissioner Management and Budget</a><br />
    <a href="/command/372" class="command">Deputy Commissioner of Public Information</a><br />
    <a href="/command/39" class="command">Deputy Commissioner of Trials</a><br />
    <a href="/command/201" class="command">Detective Borough Bronx</a><br />
    <a href="/command/181" class="command">Detective Borough Bronx Homicide Squad</a><br />
    <a href="/command/489" class="command">Detective Borough Bronx Operations</a><br />
    <a href="/command/279" class="command">Detective Borough Brooklyn North</a><br />
    <a href="/command/354" class="command">Detective Borough Brooklyn North Homicide Squad</a><br />
    <a href="/command/410" class="command">Detective Borough Brooklyn North Operations</a><br />
    <a href="/command/476" class="command">Detective Borough Brooklyn Operations</a><br />
    <a href="/command/584" class="command">Detective Borough Brooklyn South</a><br />
    <a href="/command/522" class="command">Detective Borough Brooklyn South Homicide Squad</a><br />
    <a href="/command/390" class="command">Detective Borough Manhattan North</a><br />
    <a href="/command/496" class="command">Detective Borough Manhattan North Operations</a><br />
    <a href="/command/227" class="command">Detective Borough Manhattan South</a><br />
    <a href="/command/346" class="command">Detective Borough Manhattan South Operations</a><br />
    <a href="/command/675" class="command">Detective Borough Manhattan Zone 1</a><br />
    <a href="/command/581" class="command">Detective Borough Manhattan Zone 2</a><br />
    <a href="/command/164" class="command">Detective Borough Queens Homicide Squad</a><br />
    <a href="/command/110" class="command">Detective Borough Queens North</a><br />
    <a href="/command/356" class="command">Detective Borough Queens North Operations</a><br />
    <a href="/command/378" class="command">Detective Borough Queens South</a><br />
    <a href="/command/268" class="command">Detective Borough Queens South Operations</a><br />
    <a href="/command/63" class="command">Detective Borough Queens Zone 16</a><br />
    <a href="/command/428" class="command">Detective Borough SID</a><br />
    <a href="/command/542" class="command">Detective Borough Staten Island</a><br />
    <a href="/command/245" class="command">Detective Bureau</a><br />
    <a href="/command/319" class="command">Detective Bureau Central Robbery Division</a><br />
    <a href="/command/405" class="command">Detective Bureau Criminal Enterprise Division</a><br />
    <a href="/command/260" class="command">Detective Bureau Financial Crimes Task Force</a><br />
    <a href="/command/295" class="command">Detective Bureau Grand Larceny Division</a><br />
    <a href="/command/527" class="command">Detective Bureau Gun Violence Suppression Division</a><br />
    <a href="/command/504" class="command">Detective Bureau Hate Crimes Task Force</a><br />
    <a href="/command/329" class="command">Detective Bureau Latent Print Section</a><br />
    <a href="/command/129" class="command">Detective Bureau Manhattan North Homicide Squad</a><br />
    <a href="/command/459" class="command">Detective Bureau Manhattan South Homicide Squad</a><br />
    <a href="/command/408" class="command">Detective Bureau Manhattan Special Victims Squad</a><br />
    <a href="/command/203" class="command">Detective Bureau Special Victims Division</a><br />
    <a href="/command/328" class="command">Detective Bureau Staten Island Operations</a><br />
    <a href="/command/607" class="command">Detective Bureau Transit Special Investigation Unit</a><br />
    <a href="/command/DCU" class="command">Disorder Control Unit</a><br />
    <a href="/command/351" class="command">Driver Education and Training Unit</a><br />
    <a href="/command/158" class="command">Drug Enforcement Task Force</a><br />
    <a href="/command/ESS1" class="command">Emergency Service Squad 01</a><br />
    <a href="/command/ESS2" class="command">Emergency Service Squad 02</a><br />
    <a href="/command/ESS3" class="command">Emergency Service Squad 03</a><br />
    <a href="/command/ESS4" class="command">Emergency Service Squad 04</a><br />
    <a href="/command/ESS5" class="command">Emergency Service Squad 05</a><br />
    <a href="/command/ESS6" class="command">Emergency Service Squad 06</a><br />
    <a href="/command/ESS7" class="command">Emergency Service Squad 07</a><br />
    <a href="/command/ESS8" class="command">Emergency Service Squad 08</a><br />
    <a href="/command/ESS9" class="command">Emergency Service Squad 09</a><br />
    <a href="/command/ESS10" class="command">Emergency Service Squad 10</a><br />
    <a href="/command/83" class="command">Emergency Services Unit</a><br />
    <a href="/command/708" class="command">Equal Employment Opportunity Division</a><br />
    <a href="/command/525" class="command">Equipment Section</a><br />
    <a href="/command/429" class="command">Executive Protection Unit</a><br />
    <a href="/command/647" class="command">FIS DIV</a><br />
    <a href="/command/441" class="command">Facilities Management Division</a><br />
    <a href="/command/543" class="command">Family Assistance Section</a><br />
    <a href="/command/FSS" class="command">Firearms Suppression Section</a><br />
    <a href="/command/79" class="command">Firearms and Tactics Section</a><br />
    <a href="/command/380" class="command">First Deputy Commissioner</a><br />
    <a href="/command/27" class="command">Fleet Services Division</a><br />
    <a href="/command/130" class="command">Force Investigation Division</a><br />
    <a href="/command/490" class="command">Forensics Investigations Division</a><br />
    <a href="/command/624" class="command">Fugitive Enforcement Division</a><br />
    <a href="/command/646" class="command">G&amp;B DIV</a><br />
    <a href="/command/236" class="command">Gun Violence Suppression Division Zone 01</a><br />
    <a href="/command/44" class="command">Gun Violence Suppression Division Zone 02</a><br />
    <a href="/command/97" class="command">Harbor Unit</a><br />
    <a href="/command/348" class="command">Headquarters Security</a><br />
    <a href="/command/171" class="command">Health and Wellness Section</a><br />
    <a href="/command/804" class="command">Highway STS</a><br />
    <a href="/command/151" class="command">Highway Unit 01</a><br />
    <a href="/command/262" class="command">Highway Unit 02</a><br />
    <a href="/command/84" class="command">Highway Unit 03</a><br />
    <a href="/command/259" class="command">Highway Unit 05</a><br />
    <a href="/command/464" class="command">Housing Borough Bronx/Queens Impact Response Team</a><br />
    <a href="/command/261" class="command">Housing Borough Brooklyn Impact Response Team</a><br />
    <a href="/command/563" class="command">Housing Borough Manhattan Impact Response Team</a><br />
    <a href="/command/124" class="command">Housing Bronx/Queens</a><br />
    <a href="/command/0" class="command">Housing Brooklyn</a><br />
    <a href="/command/243" class="command">Housing Bureau</a><br />
    <a href="/command/786" class="command">Housing Community Affairs Section</a><br />
    <a href="/command/123" class="command">Housing Manhattan</a><br />
    <a href="/command/590" class="command">Housing Special Operations Section</a><br />
    <a href="/command/443" class="command">Information Technology Services Division</a><br />
    <a href="/command/677" class="command">Intel-Municipal Security Section</a><br />
    <a href="/command/431" class="command">Intelligence Bureau</a><br />
    <a href="/command/305" class="command">Intelligence Bureau UOU</a><br />
    <a href="/command/424" class="command">Intelligence Division</a><br />
    <a href="/command/237" class="command">Intelligence Operations and Analysis Section</a><br />
    <a href="/command/52" class="command">Intelligence Public Security Section</a><br />
    <a href="/command/IAB" class="command">Internal Affairs Bureau</a><br />
    <a href="/command/552" class="command">Investigative Support Division</a><br />
    <a href="/command/523" class="command">Joint Bank Robbery Task Force</a><br />
    <a href="/command/112" class="command">Joint Terrorism Task Force</a><br />
    <a href="/command/557" class="command">Juvenile Crime Section</a><br />
    <a href="/command/470" class="command">Leadership Training Section</a><br />
    <a href="/command/517" class="command">Leave Integrity Management Section</a><br />
    <a href="/command/166" class="command">Legal Bureau</a><br />
    <a href="/command/88" class="command">License Division</a><br />
    <a href="/command/212" class="command">Life Safety Systems Division</a><br />
    <a href="/command/444" class="command">MODS</a><br />
    <a href="/command/142" class="command">Major Case Squad</a><br />
    <a href="/command/127" class="command">Manhattan Court Section</a><br />
    <a href="/command/50" class="command">Manhattan Robbery Squad</a><br />
    <a href="/command/753" class="command">Manhattan Standards and Assessment Unit</a><br />
    <a href="/command/324" class="command">Medical Division</a><br />
    <a href="/command/MTNdet" class="command">Midtown North Detective Squad</a><br />
    <a href="/command/MTNpct" class="command">Midtown North Precinct</a><br />
    <a href="/command/MTSdet" class="command">Midtown South Detective Squad</a><br />
    <a href="/command/MTSpct" class="command">Midtown South Precinct</a><br />
    <a href="/command/MELD" class="command">Military and Extended Leave Desk</a><br />
    <a href="/command/149" class="command">Missing Persons Squad</a><br />
    <a href="/command/1" class="command">Mounted Unit</a><br />
    <a href="/command/160" class="command">Narcotics Borough Bronx</a><br />
    <a href="/command/92" class="command">Narcotics Borough Brooklyn North</a><br />
    <a href="/command/172" class="command">Narcotics Borough Brooklyn South</a><br />
    <a href="/command/250" class="command">Narcotics Borough Manhattan North</a><br />
    <a href="/command/70" class="command">Narcotics Borough Manhattan South</a><br />
    <a href="/command/177" class="command">Narcotics Borough Queens North</a><br />
    <a href="/command/132" class="command">Narcotics Borough Queens South</a><br />
    <a href="/command/204" class="command">Narcotics Borough Staten Island</a><br />
    <a href="/command/743" class="command">OFF DB</a><br />
    <a href="/command/623" class="command">OFSCSRG</a><br />
    <a href="/command/706" class="command">OPS Emergency Prep and Exercise</a><br />
    <a href="/command/719" class="command">OPS Tactical Support Unit</a><br />
    <a href="/command/705" class="command">OPS Unit</a><br />
    <a href="/command/446" class="command">Office of Information Technology</a><br />
    <a href="/command/293" class="command">Office of Management Analysis and Planning</a><br />
    <a href="/command/628" class="command">Office of Professional Development</a><br />
    <a href="/command/734" class="command">Office of the Deputy Commissioner Management and Budget</a><br />
    <a href="/command/704" class="command">Operations Bureau</a><br />
    <a href="/command/735" class="command">Operations Division</a><br />
    <a href="/command/286" class="command">Organized Crime Drug Enforcement Strike Force</a><br />
    <a href="/command/94" class="command">Organized Crime Investigation Division</a><br />
    <a href="/command/PBBX" class="command">Patrol Borough Bronx</a><br />
    <a href="/command/760" class="command">Patrol Borough Bronx Community Affairs Section</a><br />
    <a href="/command/769" class="command">Patrol Borough Bronx Community Response Team</a><br />
    <a href="/command/722" class="command">Patrol Borough Bronx South Public Safety Teams</a><br />
    <a href="/command/45" class="command">Patrol Borough Bronx Specialized Units</a><br />
    <a href="/command/PBBN" class="command">Patrol Borough Brooklyn North</a><br />
    <a href="/command/758" class="command">Patrol Borough Brooklyn North Community Affairs Section</a><br />
    <a href="/command/767" class="command">Patrol Borough Brooklyn North Community Response Team</a><br />
    <a href="/command/720" class="command">Patrol Borough Brooklyn North Public Safety Teams</a><br />
    <a href="/command/397" class="command">Patrol Borough Brooklyn North Specialized Units</a><br />
    <a href="/command/PBBS" class="command">Patrol Borough Brooklyn South</a><br />
    <a href="/command/759" class="command">Patrol Borough Brooklyn South Community Affairs Section</a><br />
    <a href="/command/768" class="command">Patrol Borough Brooklyn South Community Response Team</a><br />
    <a href="/command/721" class="command">Patrol Borough Brooklyn South Public Safety Teams</a><br />
    <a href="/command/296" class="command">Patrol Borough Brooklyn South Specialized Units</a><br />
    <a href="/command/108" class="command">Patrol Borough Candidate Assessment Division</a><br />
    <a href="/command/619" class="command">Patrol Borough Human Resources Division</a><br />
    <a href="/command/PBMN" class="command">Patrol Borough Manhattan North</a><br />
    <a href="/command/761" class="command">Patrol Borough Manhattan North Community Affairs Section</a><br />
    <a href="/command/770" class="command">Patrol Borough Manhattan North Community Response Team</a><br />
    <a href="/command/723" class="command">Patrol Borough Manhattan North Public Safety Teams</a><br />
    <a href="/command/178" class="command">Patrol Borough Manhattan North Specialized Units</a><br />
    <a href="/command/PBMS" class="command">Patrol Borough Manhattan South</a><br />
    <a href="/command/762" class="command">Patrol Borough Manhattan South Community Affairs Section</a><br />
    <a href="/command/771" class="command">Patrol Borough Manhattan South Community Response Team</a><br />
    <a href="/command/724" class="command">Patrol Borough Manhattan South Public Safety Teams</a><br />
    <a href="/command/104" class="command">Patrol Borough Manhattan South Specialized Units</a><br />
    <a href="/command/498" class="command">Patrol Borough POD</a><br />
    <a href="/command/PBQN" class="command">Patrol Borough Queens North</a><br />
    <a href="/command/763" class="command">Patrol Borough Queens North Community Affairs Section</a><br />
    <a href="/command/772" class="command">Patrol Borough Queens North Community Response Team</a><br />
    <a href="/command/725" class="command">Patrol Borough Queens North Public Safety Teams</a><br />
    <a href="/command/256" class="command">Patrol Borough Queens North Specialized Units</a><br />
    <a href="/command/PBQS" class="command">Patrol Borough Queens South</a><br />
    <a href="/command/764" class="command">Patrol Borough Queens South Community Affairs Section</a><br />
    <a href="/command/773" class="command">Patrol Borough Queens South Community Response Team</a><br />
    <a href="/command/726" class="command">Patrol Borough Queens South Public Safety Teams</a><br />
    <a href="/command/481" class="command">Patrol Borough Queens South Specialized Units</a><br />
    <a href="/command/332" class="command">Patrol Borough SAS</a><br />
    <a href="/command/PBSI" class="command">Patrol Borough Staten Island</a><br />
    <a href="/command/765" class="command">Patrol Borough Staten Island Community Affairs Section</a><br />
    <a href="/command/774" class="command">Patrol Borough Staten Island Community Response Team</a><br />
    <a href="/command/463" class="command">Patrol Borough Staten Island Specialized Units</a><br />
    <a href="/command/766" class="command">Patrol Service Bureau Community Response Team</a><br />
    <a href="/command/488" class="command">Patrol Services Bureau</a><br />
    <a href="/command/309" class="command">Patrol Services Bureau IES</a><br />
    <a href="/command/540" class="command">Patrol Services Bureau Movie and T.V. Unit</a><br />
    <a href="/command/561" class="command">Patrol Services Bureau Resource Management Section</a><br />
    <a href="/command/806" class="command">Patrol Services Bureau Wheel</a><br />
    <a href="/command/629" class="command">Payroll and Benefits Division</a><br />
    <a href="/command/456" class="command">Personnel Bureau</a><br />
    <a href="/command/310" class="command">Police Academy Payroll and Roll Call</a><br />
    <a href="/command/271" class="command">Police Cadet Corps Unit</a><br />
    <a href="/command/422" class="command">Police Commissioner Office</a><br />
    <a href="/command/78" class="command">Police Laboratory</a><br />
    <a href="/command/532" class="command">Police Pension Fund</a><br />
    <a href="/command/PSA1" class="command">Police Service Area 1</a><br />
    <a href="/command/PSA2" class="command">Police Service Area 2</a><br />
    <a href="/command/PSA3" class="command">Police Service Area 3</a><br />
    <a href="/command/PSA4" class="command">Police Service Area 4</a><br />
    <a href="/command/PSA5" class="command">Police Service Area 5</a><br />
    <a href="/command/PSA6" class="command">Police Service Area 6</a><br />
    <a href="/command/PSA7" class="command">Police Service Area 7</a><br />
    <a href="/command/PSA8" class="command">Police Service Area 8</a><br />
    <a href="/command/PSA9" class="command">Police Service Area 9</a><br />
    <a href="/command/787" class="command">Professional Standards Bureau</a><br />
    <a href="/command/106" class="command">Property Clerk Division</a><br />
    <a href="/command/550" class="command">Quality Assurance</a><br />
    <a href="/command/750" class="command">Quality Assurance Division</a><br />
    <a href="/command/59" class="command">Quartermaster Section</a><br />
    <a href="/command/176" class="command">Queens Court Section</a><br />
    <a href="/command/290" class="command">Queens Robbery Squad</a><br />
    <a href="/command/51" class="command">Queens Special Victims Squad</a><br />
    <a href="/command/752" class="command">Queens Standards and Assessment Unit</a><br />
    <a href="/command/375" class="command">Real Time Crime Center</a><br />
    <a href="/command/333" class="command">Recruit Training Section</a><br />
    <a href="/command/347" class="command">Risk Management Bureau CD</a><br />
    <a href="/command/257" class="command">Risk Management Bureau Quality Assurance Division</a><br />
    <a href="/command/13" class="command">School Safety Division</a><br />
    <a href="/command/785" class="command">School Safety Division Youth Response Team</a><br />
    <a href="/command/238" class="command">Special Fraud Squad</a><br />
    <a href="/command/811" class="command">Special Investigations Unit</a><br />
    <a href="/command/503" class="command">Special Victims Division Zone 1</a><br />
    <a href="/command/472" class="command">Special Victims Division Zone 3</a><br />
    <a href="/command/77" class="command">Specialized Training Section</a><br />
    <a href="/command/244" class="command">Staten Island Court Section</a><br />
    <a href="/command/717" class="command">Staten Island Special Victims Squad</a><br />
    <a href="/command/756" class="command">Staten Island Standards and Assessment Unit</a><br />
    <a href="/command/738" class="command">Strategic Initiatives Bureau</a><br />
    <a href="/command/SRG" class="command">Strategic Response Group</a><br />
    <a href="/command/SRG1" class="command">Strategic Response Group 1 Manhattan</a><br />
    <a href="/command/SRG2" class="command">Strategic Response Group 2 Bronx</a><br />
    <a href="/command/SRG3" class="command">Strategic Response Group 3 Brooklyn</a><br />
    <a href="/command/SRG4" class="command">Strategic Response Group 4 Queens</a><br />
    <a href="/command/SRG5" class="command">Strategic Response Group 5 Staten Island</a><br />
    <a href="/command/731" class="command">Strategic Response Group Crowd Management Unit</a><br />
    <a href="/command/335" class="command">Strategic Technology Division</a><br />
    <a href="/command/TARU" class="command">Technical Assistance and Response Unit</a><br />
    <a href="/command/485" class="command">Training Bureau</a><br />
    <a href="/command/535" class="command">Transit Authority Liaison</a><br />
    <a href="/command/TB" class="command">Transit Bureau</a><br />
    <a href="/command/153" class="command">Transit Bureau Anti-Terrorism Unit</a><br />
    <a href="/command/560" class="command">Transit Bureau Bronx/Queens</a><br />
    <a href="/command/357" class="command">Transit Bureau Brooklyn</a><br />
    <a href="/command/484" class="command">Transit Bureau Brooklyn Task Force</a><br />
    <a href="/command/790" class="command">Transit Bureau Bus Enforcement Unit</a><br />
    <a href="/command/445" class="command">Transit Bureau Canine Unit</a><br />
    <a href="/command/199" class="command">Transit Bureau Citywide Vandals Task Force</a><br />
    <a href="/command/602" class="command">Transit Bureau Crime Analysis</a><br />
    <a href="/command/TB1" class="command">Transit Bureau District 1</a><br />
    <a href="/command/TB11" class="command">Transit Bureau District 11</a><br />
    <a href="/command/TB12" class="command">Transit Bureau District 12</a><br />
    <a href="/command/TB2" class="command">Transit Bureau District 2</a><br />
    <a href="/command/TB20" class="command">Transit Bureau District 20</a><br />
    <a href="/command/TB23" class="command">Transit Bureau District 23</a><br />
    <a href="/command/TB3" class="command">Transit Bureau District 3</a><br />
    <a href="/command/TB30" class="command">Transit Bureau District 30</a><br />
    <a href="/command/TB32" class="command">Transit Bureau District 32</a><br />
    <a href="/command/TB33" class="command">Transit Bureau District 33</a><br />
    <a href="/command/TB34" class="command">Transit Bureau District 34</a><br />
    <a href="/command/TB4" class="command">Transit Bureau District 4</a><br />
    <a href="/command/569" class="command">Transit Bureau Manhattan</a><br />
    <a href="/command/99" class="command">Transit Bureau Manhattan Task Force</a><br />
    <a href="/command/783" class="command">Transit Bureau Response Team</a><br />
    <a href="/command/396" class="command">Transit Bureau Special Operations District</a><br />
    <a href="/command/733" class="command">Transit Bureau Subway Safety Task Force</a><br />
    <a href="/command/757" class="command">Transit Standards and Assessment Unit</a><br />
    <a href="/command/366" class="command">Transportation Bureau</a><br />
    <a href="/command/75" class="command">Transportation Bureau Citywide Traffic</a><br />
    <a href="/command/81" class="command">Transportation Bureau Highway District</a><br />
    <a href="/command/307" class="command">Transportation Bureau Traffic Enforcement District</a><br />
    <a href="/command/398" class="command">Uniformed Promotions Training Unit</a><br />
    <a href="/command/207" class="command">Vice Enforcement Squad MCS</a><br />
    <a href="/command/303" class="command">Vice Enforcement Squad Zone 1</a><br />
    <a href="/command/248" class="command">Vice Enforcement Squad Zone 2</a><br />
    <a href="/command/118" class="command">Warrant Section</a><br />
    <a href="/command/141" class="command">World Trade Center Command</a><br />
    <a href="/command/471" class="command">Youth Strategies Division</a><br />
  </div>
</section>

    <footer>
      <a href="/">50-a.org</a> &mdash;
      <a href="/about">About</a> &mdash;
      <a href="https://www.nyc.gov/site/ccrb/complaints/file-a-complaint/file-online.page">File a complaint</a>
    </footer>
  </body>
</html>
"""
